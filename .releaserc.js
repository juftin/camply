const path = require("path");
const fs = require("fs");

const semantic_release_dir = path.resolve(__dirname, ".github/semantic_release");
const release_note_path = path.join(semantic_release_dir, "release_notes.hbs");
const release_note_template = fs.readFileSync(release_note_path, "utf-8");

module.exports = {
    branches: [
        "main",
        "master",
        "next",
        "next-major",
        "+([0-9])?(.{+([0-9]),x}).x",
        {
            name: "beta",
            prerelease: true,
        },
        {
            name: "alpha",
            prerelease: true,
        },
    ],
    plugins: [
        [
            "semantic-release-gitmoji",
            {
                releaseNotes: {
                    template: release_note_template,
                },
            },
        ],
        [
            "@semantic-release/exec",
            {
                prepareCmd: "hatch version ${nextRelease.version} && hatch build",
            },
        ],
        [
            "@semantic-release/git",
            {
                assets: ["pyproject.toml", "*/_version.py"],
                message:
                    "🔖 camply ${nextRelease.version}\n\n${nextRelease.notes}\n[skip ci]",
            },
        ],
        [
            "@semantic-release/github",
            {
                assets: [
                    {
                        path: "dist/*.whl",
                    },
                    {
                        path: "dist/*.tar.gz",
                    },
                ],
            },
        ],
    ],
};
