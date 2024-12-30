
import aiohttp
from pathlib import Path
from mimetypes import guess_extension
import os

async def get_text_file(url, cookies=None):
    """Asynchronously download a text file from a URL and return its content as a string."""
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.get(url, allow_redirects=True) as response:
            if response.status != 200:
                raise Exception(f"Failed to download file. HTTP Status: {response.status}")
            
            # Read the response content as text
            content = await response.text()
            return content

async def download_file(url, directory, cookies=None):
    """Asynchronously download a file from a URL and save it to the specified directory."""
    async with aiohttp.ClientSession(cookies=cookies) as session:
        async with session.get(url, allow_redirects=True) as response:
            # Check if content-disposition is set
            if 'content-disposition' in response.headers:
                filename = response.headers['content-disposition'].split("filename=")[1]
                filename = filename.replace('"', '')
            else:
                # Get filename from URL
                filename = Path(url).stem
                if not filename:
                    filename = "file"
                # Get extension from content-type
                content_type = response.headers.get('content-type', '').split(";")[0]
                ext = guess_extension(content_type, strict=False)
                filename += ext if ext else '.bin'

            # Prepare file path
            file_path = Path(directory) / filename
            os.makedirs(directory, exist_ok=True)

            # Write content to file in chunks
            with open(file_path, 'wb') as fd:
                async for chunk in response.content.iter_chunked(8192):
                    fd.write(chunk)

            return file_path