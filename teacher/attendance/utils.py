from academics.schoolclass.models import SchoolClass


def get_leafnodes(root):
    nodes = SchoolClass.objects.all()

    children_map = {}
    for node in nodes:
        children_map.setdefault(node.parent_id, []).append(node)

    leaves = []

    def dfs(node):
        children = children_map.get(node.id, [])
        if not children:
            leaves.append(node)
            return

        for child in children:
            dfs(child)

    dfs(root)
    return leaves