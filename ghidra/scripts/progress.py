# Prints the percentage of functions already renamed
fm = currentProgram.getFunctionManager()
functions = fm.getFunctions(True)

fn_count = 0
total = 0
for f in functions:
    if f.parentNamespace.isLibrary():
        continue
    if f.name.startswith('FUN_'):
        fn_count += 1
    total += 1


print(fn_count)
print(other)
print(100 - ((fn_count*100)/total))
