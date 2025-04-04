// frontend/src/utils/shortcuts.ts
export const handleEnter = (e: React.KeyboardEvent, action: () => void) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        action();
    }
};