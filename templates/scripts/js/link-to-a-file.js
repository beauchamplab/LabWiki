module.exports = async (params) => {
    const { app, quickAddApi, variables } = params;
    
    // Get current file
    const currentFile = app.workspace.getActiveFile();
    if (!currentFile) {
        new Notice('No active file. Please open a note first.');
        return;
    }
    
    // Get all files in vault (excluding current file)
    const allFiles = app.vault.getFiles().filter(f => f.path !== currentFile.path);
    
    if (allFiles.length === 0) {
        new Notice('No other files found in vault.');
        return;
    }
    
    // Create suggester options
    const fileNames = allFiles.map(f => f.path);
    
    // Let user select file(s)
    const selectedPath = await quickAddApi.suggester(fileNames, allFiles);
    
    if (!selectedPath) {
        // User cancelled
        return;
    }
    
    // Get selected text from editor (if any)
    const editor = app.workspace.activeLeaf.view.editor;
    const selectedText = editor.getSelection();
    
    // Determine link text
    let linkText;
    if (selectedText && selectedText.trim()) {
        linkText = selectedText.trim();
    } else {
        // Use filename without extension
        linkText = selectedPath.basename;
    }
    
    // Calculate relative path
    const currentFilePath = currentFile.parent.path;
    const targetFilePath = selectedPath.path;
    const relativePath = getRelativePath(currentFilePath, targetFilePath);
    
    // Create markdown link
    const markdownLink = `[${linkText}](${relativePath})`;
    
    // Store in variable for capture
    variables.fileLink = markdownLink;
    
    // If there was selected text, we'll replace it, otherwise insert
    if (selectedText && selectedText.trim()) {
        editor.replaceSelection(markdownLink);
    }
};

function getRelativePath(fromPath, toPath) {
    // Split paths into parts
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