with open("numbered_lines.txt", "w") as f:
    for i in range(1, 1001):
        f.write(f"Line {i:04d}\n")
