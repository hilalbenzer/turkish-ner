
def replace_digit(word):
	return "".join(["#" if char.isdigit() else char for char in word])

sentences = []
with open('newscor.txt', 'r', encoding="utf-8", errors="ignore") as f:
	line_count = 0
	for line in f:
		print(str(line_count) + "/20064430")
		words = line.split()
		new_words = []
		for word in words:
			new_words.append(replace_digit(word))
		sentences.append(" ".join(new_words))
		line_count += 1

with open('newscor_digitless.txt', 'w', encoding="utf-8", errors="ignore") as f:
	for sentence in sentences:
		f.write(sentence)
		f.write("\n")
