import aiofiles
import asyncio
import shutil


async def remove_lines(file_path, lines_to_remove: list):
    # Read the file content asynchronously
    async with aiofiles.open(file_path, 'r') as file:
        lines = await file.readlines()

    # Filter out the specific lines to remove
    lines = [line for line in lines if line.strip() not in lines_to_remove]

    # Write the modified content back to the file asynchronously
    async with aiofiles.open(file_path, 'w') as file:
        await file.writelines(lines)


async def unregister_model(folder_name: str, class_name: str):
    filepath = f"app/models/register_models.py"
    # Lines to remove
    lines_to_remove = [
        f"from .{folder_name}.models import {class_name}"
    ]
    await remove_lines(filepath, lines_to_remove)


async def unregister_api(folder_name, class_name):
    filepath = f"app/controllers/register_api.py"
    # Lines to remove
    lines_to_remove = [
        f"from .v1.{folder_name}.api import router as {folder_name}_router",
        f"router.include_router({folder_name}_router, tags=[\"{class_name}\"])"
    ]
    await remove_lines(filepath, lines_to_remove)


async def unregister():
    folder_name = input("Remove folder name: ").lower().replace(" ", "_")
    class_name = input("Remove class name: ").title()
    await unregister_model(folder_name, class_name)
    await unregister_api(folder_name, class_name)
    shutil.rmtree(f"app/models/{folder_name}")
    shutil.rmtree(f"app/controllers/v1/{folder_name}")
    shutil.rmtree(f"app/services/{folder_name}")
    shutil.rmtree(f"app/repositories/{folder_name}")
    shutil.rmtree(f"app/schemas/{folder_name}")


# Run the async function
if __name__ == "__main__":
    asyncio.run(unregister())
