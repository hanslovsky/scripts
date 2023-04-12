#!/usr/bin/env kscript

@file:DependsOn("com.drewnoakes:metadata-extractor:2.13.0")
@file:DependsOn("org.apache.commons:commons-lang3:3.10")
@file:DependsOn("info.picocli:picocli:4.2.0")

import java.io.File
import java.nio.file.CopyOption
import java.nio.file.StandardCopyOption
import java.nio.file.Files
import java.text.SimpleDateFormat
import java.util.concurrent.Callable

import com.drew.imaging.ImageMetadataReader
import com.drew.metadata.Metadata
import com.drew.metadata.exif.ExifDirectoryBase
import com.drew.metadata.exif.ExifIFD0Directory
import org.apache.commons.lang3.builder.ToStringBuilder
import picocli.CommandLine

fun File.prefixName(prefix: String) = updateName { "$prefix$it" }

fun File.updateName(nameUpdate: (String) -> String) = File(parent, nameUpdate(name))

@CommandLine.Command(name = "rn-exif-date", description = ["Rename image files using exif date."])
class RenameArgs : Callable<Int> {

    enum class ExifTag(val tag: Int) {
        DATETIME(ExifDirectoryBase.TAG_DATETIME),
        DATETIME_ORIGINAL(ExifDirectoryBase.TAG_DATETIME_ORIGINAL),
        DATETIME_DIGITIZED(ExifDirectoryBase.TAG_DATETIME_DIGITIZED)
    }

    private val tagDateFormat = SimpleDateFormat("yyyy:MM:dd HH:mm:ss")

    @CommandLine.Option(names = ["--dry-run", "-d"], required = false, description = ["Do not do anything. Use in conjunction with the `--verbose' flag to print what would happen."])
    private var dryRun: Boolean = false

    @CommandLine.Parameters(arity = "*", description = ["List of image files to be renamed"])
    private var files: MutableList<File> = mutableListOf()

    @CommandLine.Option(names = ["--exif-tag-type", "-t"], required = false, defaultValue = "DATETIME")
    private lateinit var tagType: ExifTag

    @CommandLine.Option(names = ["--format", "-f"], required = false, defaultValue = "yyyyMMdd_HHmmss_", description=["Date will be formatted and prefixed to filename."])
    private lateinit var outputFormatString: String

    @CommandLine.Option(names = ["--overwrite-existing", "-o"], required = false, description = ["Overwrite existing target files. Will fail if not specified and target files exist."])
    private var overwriteExisting = false

    @CommandLine.Option(names = ["--verbose"], required = false)
    private var verbose = false

    @CommandLine.Option(names = ["--keep-original", "-k"], required = false, description = ["Copy instead of moving (keep original)."])
    private var copy = false

    override fun call(): Int {
        val filesToMeta = mutableMapOf<File, Metadata>()

        val filesWithoutMetaData = mutableMapOf<File, Exception>()

        val uniqueFiles: List<File> = files.filter { file: File -> 
            if (file in filesToMeta) false
            else {
                try {
                    filesToMeta[file] = ImageMetadataReader.readMetadata(file)
                    true
                } catch(exception: Exception) {
                    filesWithoutMetaData[file] = exception
                    false
                }
            }
        }

        val filesToDateTime = filesToMeta.mapValues {
            try {
                it
                        .value
                        .getDirectoriesOfType(ExifIFD0Directory::class.java)
                        .flatMap { it.tags }
                        .filter { it.tagType == tagType.tag }
                        .also { if (it.isEmpty()) throw Exception("Tag `${tagType}' not found.") }
                        .first()
                        .description
                        .let { tagDateFormat.parse(it) }
            } catch(exception: Exception) {
                filesWithoutMetaData[it.key] = exception
            }
        }

        filesWithoutMetaData.takeIf { it.isNotEmpty() }?.let {
            throw Exception("Unable to extract meta data from files:\n${it.entries.map{ "`${it.key}': ${it.value.message}" }.joinToString("\n")}")
        }

        val outputDateFormat = SimpleDateFormat(outputFormatString)

        val filesToNewFiles = filesToDateTime.mapValues { it.key.prefixName(outputDateFormat.format(it.value)) }

        filesToNewFiles.values.filter { it.exists() }.takeIf { it.isNotEmpty() && !overwriteExisting }?.let {
            throw Exception("Output files already exist:\n${it.joinToString("\n")}\nUse the `--overwrite-existing / -o' flag to force overwrite.")
        }

        val copyOptions = if (overwriteExisting) arrayOf(StandardCopyOption.REPLACE_EXISTING) else arrayOf<CopyOption>()

        uniqueFiles.forEach { file ->
            if (verbose)
                println("`$file' --${if (copy) "copy" else "move"}--> `${filesToNewFiles[file]}'")

            if (!dryRun) {
                if (copy) {
                    Files.copy(file.toPath(), filesToNewFiles[file]!!.toPath(), *copyOptions)
                } else
                    Files.move(file.toPath(), filesToNewFiles[file]!!.toPath(), *copyOptions)
            }
        }
        
        return 0
    }

    override fun toString() = ToStringBuilder(this)
            .append("dryRun", dryRun)
            .append("files", files)
            .toString()

}

val errorHandler = CommandLine.IExecutionExceptionHandler { exception, commandLine, parseResult ->
    commandLine.getErr().println(exception.message)
    commandLine.getErr().println()
    commandLine.usage(commandLine.getErr())
    commandLine.getCommandSpec().exitCodeOnExecutionException()
}

val exitCode = CommandLine(RenameArgs())
        .setExecutionExceptionHandler(errorHandler)
        .execute(*args)
kotlin.system.exitProcess(exitCode)
