import os

instance_sizes = ["5_3", "200_50", "1000_100", "2000_500", "2500_1000", "5000_1500"]
instance_hardness = ["EASY", "MEDIUM", "HARD"]

for isize in instance_sizes:
	for hardness in instance_hardness:
		print(f"{hardness}: {isize}")
		os.system(f"/Applications/MiniZincIDE.app/Contents/Resources/minizinc Model_{hardness}.mzn Instances/{hardness}_{isize}.dzn -o sol_{hardness}_{isize}.txt -O0 --time-limit 3600000")