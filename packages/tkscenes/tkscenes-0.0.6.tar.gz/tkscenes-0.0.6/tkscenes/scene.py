from tkscenes.child import Child as Child


class Scene:
    def __init__(self):
        self.children: dict[str, Child] = {}

    def __setitem__(self, key, value):
        self.children[key] = Child(value)

    def __getitem__(self, item):
        return self.children[item]

    def load(self):
        for child in self.children.values():
            child.render()

    def unload(self):
        for child in self.children.values():
            child.unrender()

    def destroy(self):
        for key in self.children.keys():
            self.children[key].destroy()
