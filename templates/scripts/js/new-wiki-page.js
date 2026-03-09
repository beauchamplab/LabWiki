module.exports = async (params) => {
    const { app, quickAddApi } = params;

    // Category definitions: display name, folder path, frontmatter parent, grand_parent
    const categories = [
        { label: "Data Processing and Analysis", folder: "pages/Beauchamp/Data_Processing", parent: "Data Processing and Analysis", grandParent: "Beauchamp" },
        { label: "Lab Meetings and Notes",       folder: "pages/Beauchamp/Lab_Meetings_and_Notes", parent: "Lab Meetings and Notes", grandParent: "Beauchamp" },
        { label: "Publications and Talks",       folder: "pages/Beauchamp/Publications_and_Talks", parent: "Publications and Talks", grandParent: "Beauchamp" },
        { label: "Resources and Data Sharing",   folder: "pages/Beauchamp/Resources_and_Data_Sharing", parent: "Resources and Data Sharing", grandParent: "Beauchamp" },
        { label: "Obsolete",                     folder: "pages/Beauchamp/Obsolete", parent: "Obsolete", grandParent: "Beauchamp" },
        { label: "Internal Notes",              folder: "pages/Beauchamp/Internal_Notes", parent: "Internal Notes", grandParent: "Beauchamp" },
    ];

    // 1. Choose category
    const category = await quickAddApi.suggester(
        categories.map(c => c.label),
        categories,
        "Choose a category for the new page"
    );
    if (!category) return;

    // 2. Prompt for page title
    const topic = await quickAddApi.inputPrompt("Page title (used as heading)");
    if (!topic) return;

    // 3. Auto-generate filename: replace non-alphanumeric chars with underscores
    const fileName = topic.replace(/[^a-zA-Z0-9]+/g, '_').replace(/^_|_$/g, '') + '.md';
    const filePath = `${category.folder}/${fileName}`;

    // Check if file already exists
    if (app.vault.getAbstractFileByPath(filePath)) {
        new Notice(`File already exists: ${filePath}`);
        return;
    }

    // Ensure target folder exists
    await ensureFolder(app, category.folder);

    // 4. Build frontmatter
    const today = formatDate(new Date());
    let frontmatter = `---\nlayout: default\ntitle: "${topic}"\ndate_created: "${today}"\n`;
    frontmatter += `parent: ${category.parent}\n`;
    if (category.grandParent) {
        frontmatter += `grand_parent: ${category.grandParent}\n`;
    }
    frontmatter += `---\n`;

    // 5. Build Quick Access links (relative paths differ for root vs subfolder)
    const isRoot = category.grandParent === null;
    const prefix = isRoot ? "" : "../";
    const quickAccess = [
        `> Quick Access`,
        `> - [Home](${prefix}index.md "Beauchamp")`,
        `> - [Publications](${prefix}Publications_and_Talks/Publications.md "Beauchamp:Publications")`,
        `> - [Resources](${prefix}Resources_and_Data_Sharing/DataSharing.md "Beauchamp:DataSharing")`,
    ].join('\n');

    // 6. Read cheat-sheet portion from the template
    let cheatSheet = "";
    const templateFile = app.vault.getAbstractFileByPath("templates/template.md");
    if (templateFile) {
        const templateContent = await app.vault.read(templateFile);
        const marker = "# Quick Markdown Cheat Sheet";
        const idx = templateContent.indexOf(marker);
        if (idx !== -1) {
            cheatSheet = templateContent.substring(idx);
        }
    }

    // 7. Assemble full content
    const content = [
        frontmatter,
        `# ${topic}`,
        "",
        quickAccess,
        "",
        `_Date created: ${today}_`,
        "",
        "",
        "",
        "",
        cheatSheet,
    ].join('\n');

    // 8. Create the file
    const newFile = await app.vault.create(filePath, content);

    // 9. Open the new file
    const leaf = app.workspace.getLeaf(false);
    await leaf.openFile(newFile);
};

// ---------- helpers ----------

async function ensureFolder(app, path) {
    const parts = path.split('/');
    let current = '';
    for (const part of parts) {
        current = current ? `${current}/${part}` : part;
        if (!app.vault.getAbstractFileByPath(current)) {
            await app.vault.createFolder(current);
        }
    }
}

function formatDate(date) {
    const y = date.getFullYear();
    const m = String(date.getMonth() + 1).padStart(2, '0');
    const d = String(date.getDate()).padStart(2, '0');
    return `${y}-${m}-${d}`;
}
