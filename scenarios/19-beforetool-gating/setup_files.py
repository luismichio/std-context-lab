import os
with open("massive_50mb.log", "w") as f:
    f.write("A" * 50 * 1024 * 1024)
with open("threshold_limit.log", "w") as f:
    f.write("A" * 1000)
with open("small_config.json", "w") as f:
    f.write("{\"key\": \"value\"}")
