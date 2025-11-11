import { NextRequest, NextResponse } from "next/server"
import { writeFile, mkdir, readdir, unlink } from "fs/promises"
import { existsSync } from "fs"
import path from "path"

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData()
    const resumeFile = formData.get("resume") as File
    const jobDescription = formData.get("jobDescription") as string

    if (!resumeFile || !jobDescription) {
      return NextResponse.json(
        { error: "Resume file and job description are required" },
        { status: 400 }
      )
    }

    // Get the project root directory (3 levels up from app/api/upload)
    const projectRoot = path.join(process.cwd(), "..")
    const assetsDir = path.join(projectRoot, "assets")

    // Create assets directory if it doesn't exist
    if (!existsSync(assetsDir)) {
      await mkdir(assetsDir, { recursive: true })
    }

    // Clean the assets directory (delete all existing files)
    const existingFiles = await readdir(assetsDir)
    for (const file of existingFiles) {
      await unlink(path.join(assetsDir, file))
    }

    // Save the resume file with the format resume.{extension}
    const resumeBuffer = Buffer.from(await resumeFile.arrayBuffer())
    const fileExtension = path.extname(resumeFile.name)
    const resumeFileName = `resume${fileExtension}`
    const resumePath = path.join(assetsDir, resumeFileName)
    await writeFile(resumePath, resumeBuffer)

    // Save the job description as job.txt
    const jobDescFileName = `job.txt`
    const jobDescPath = path.join(assetsDir, jobDescFileName)
    await writeFile(jobDescPath, jobDescription, "utf-8")

    return NextResponse.json(
      {
        message: "Files uploaded successfully",
        resumeFile: resumeFileName,
        jobDescFile: jobDescFileName,
      },
      { status: 200 }
    )
  } catch (error) {
    console.error("Upload error:", error)
    return NextResponse.json(
      { error: "Failed to upload files" },
      { status: 500 }
    )
  }
}