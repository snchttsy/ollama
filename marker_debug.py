import subprocess

cmd = [
    "py", "-3.11", "-m", "marker.scripts.convert_single",
    "test.pdf",
    "--output_format", "markdown",
    "--output_path", "output.md"
]

print("Запускаем marker...")
result = subprocess.run(cmd, capture_output=True, text=True)
print("STDOUT:\n", result.stdout)
print("STDERR:\n", result.stderr)
