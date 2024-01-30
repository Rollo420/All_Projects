hello = input("Bitte ein input machen:\n")
count = 0

for i in range(0, len(hello)):
    print(hello[i])
    count+=1

print(f"Ihr wort hat {len(hello)} zeichen")
