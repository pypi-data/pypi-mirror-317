from tkscenes.child import Child as Child


class Scene:
    def __init__(self):
        """
        Create a new scene
        """
        self.children: dict[str, Child] = {}

    def __setitem__(self, key: str, value) -> None:
        """
        Add or modify a new widget to scene
        :param key: Identifier
        :param value: The widget you want to add to the scene
        :return:
        """
        self.children[key] = Child(value)

    def __getitem__(self, item) -> Child:
        """
        Get a child with the identifier
        :param item: Identifier
        :return: Returns a child object
        """
        return self.children[item]

    def load(self) -> None:
        """
        Load the scene
        :return:
        """
        for child in self.children.values():
            child.render()

    def unload(self) -> None:
        """
        Unload the scene
        :return:
        """
        for child in self.children.values():
            child.unrender()

    def destroy(self) -> None:
        """
        Removes the scene and destroy all it's child
        :return:
        """
        keys = list(self.children.keys())

        for key in keys:
            self.children[key].destroy()
            del self.children[key]
