module.exports = async (params) => {
    const { app, quickAddApi, variables } = params;
    
    // Let user choose attachment folder
    const folderChoice = await quickAddApi.suggester(
        ['Large Files', 'Small Files', 'Publications'],
        ['attachments/Shared', 'attachments/SmallFiles', 'attachments/Publications'],
        'Where do you want to save the files?'
    );
    
    if (!folderChoice) {
        // User cancelled
        return;
    }
    
    const ATTACHMENT_FOLDER = folderChoice;
    
    const files = await selectMultipleFiles();
    if (!files || files.length === 0) return;
    
    await ensureFolder(app, ATTACHMENT_FOLDER);
    
    const links = [];
    
    // Get current file path for relative path calculation
    const currentFile = app.workspace.getActiveFile();
    if (!currentFile) {
        new Notice('No active file. Please open or create a note first.');
        return;
    }
    const currentFilePath = currentFile.parent.path;
    
    for (const file of files) {
        const cleanName = file.name.replace(/[^a-zA-Z0-9.-]/g, '_');
        let finalName = cleanName;
        
        // Check if file already exists
        const existingPath = `${ATTACHMENT_FOLDER}/${cleanName}`;
        const existingFile = app.vault.getAbstractFileByPath(existingPath);
        
        if (existingFile) {
            const choice = await quickAddApi.suggester(
                ['Overwrite existing file', 'Rename with date'],
                ['overwrite', 'rename'],
                `File "${cleanName}" already exists. What would you like to do?`
            );
            
            if (!choice) {
                // User cancelled, skip this file
                continue;
            }
            
            if (choice === 'overwrite') {
                // Delete existing file
                await app.vault.delete(existingFile);
                finalName = cleanName;
            } else if (choice === 'rename') {
                // Rename with YYMMDD format
                const now = new Date();
                const dateStr = formatDate(now);
                
                const nameParts = cleanName.split('.');
                const ext = nameParts.pop();
                const base = nameParts.join('.');
                finalName = `${base}_${dateStr}.${ext}`;
                
                // Check if renamed file also exists (unlikely but possible)
                let counter = 1;
                while (app.vault.getAbstractFileByPath(`${ATTACHMENT_FOLDER}/${finalName}`)) {
                    finalName = `${base}_${dateStr}_${counter}.${ext}`;
                    counter++;
                }
            }
        }
        
        const filepath = `${ATTACHMENT_FOLDER}/${finalName}`;
        
        const arrayBuffer = await file.arrayBuffer();
        await app.vault.createBinary(filepath, arrayBuffer);
        
        // Calculate relative path from current file to attachment
        const relativePath = getRelativePath(currentFilePath, filepath);
        links.push(`[${file.name}](${relativePath})`);
    }
    
    if (links.length === 0) {
        new Notice('No files were attached.');
        return;
    }
    
    // Store as variable for template
    variables.attachments = links.join('\n');
    
    new Notice(`Attached ${links.length} file(s) to ${ATTACHMENT_FOLDER}`);
};

function formatDate(date) {
    const yy = date.getFullYear().toString().slice(-2);
    const mm = String(date.getMonth() + 1).padStart(2, '0');
    const dd = String(date.getDate()).padStart(2, '0');
    return `${yy}${mm}${dd}`;
}

function getRelativePath(fromPath, toPath) {
    // Both paths should be folder paths (not including filename)
    const fromParts = fromPath.split('/').filter(p => p);
    const toParts = toPath.split('/').filter(p => p);
    
    // Find common base
    let commonLength = 0;
    while (
        commonLength < fromParts.length &&
        commonLength < toParts.length &&
        fromParts[commonLength] === toParts[commonLength]
    ) {
        commonLength++;
    }
    
    // Calculate how many levels to go up
    const upLevels = fromParts.length - commonLength;
    
    // Build relative path
    const upPath = upLevels > 0 ? '../'.repeat(upLevels) : './';
    const downPath = toParts.slice(commonLength).join('/');
    
    return upPath + downPath;
}

async function selectMultipleFiles() {
    return new Promise((resolve) => {
        const input = document.createElement('input');
        input.type = 'file';
        input.multiple = true;
        
        input.onchange = (e) => {
            const files = Array.from(e.target.files);
            resolve(files);
        };
        
        input.click();
    });
}

async function ensureFolder(app, path) {
    const folder = app.vault.getAbstractFileByPath(path);
    if (!folder) {
        await app.vault.createFolder(path);
    }
}