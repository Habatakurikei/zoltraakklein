import time
from zoltraakklein import ZoltraakKlein
from zoltraakklein.yaml_manager import YAMLManager


zk = ZoltraakKlein(
    request="Short-hair Japanese bartender girl in 20s, anime-style",
    compiler="virtual_human",
    verbose=True
)

# Step 1: Name the requirement
zk.name_for_requirement()

# Step 2: Generate the requirement
zk.generate_requirement()

# Step 3: Expand the domain
while zk.is_expansion_capable():
    try:
        zk.expand_domain()
        while zk.expansion_in_progress:
            time.sleep(1)
    except Exception as e:
        print(e)
        break

# Show the result
if zk.project_menu.exists():
    menu = YAMLManager(str(zk.project_menu))
    print('Menu (list of generated items) is ready.')
    print(zk.project_menu.read_text(encoding="utf-8"))
    print(f'Total {menu.sum_of_items()} files generated.')

print(f'Elapsed time for each step (sec):')
for step, elapsed_time in zk.takt_time.items():
    print(f"    {step}: {elapsed_time}")
print(f'Total elapsed time (sec) = {sum(zk.takt_time.values())}')
