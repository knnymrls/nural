import uuid


class Contribution:
    def __init__(self, person, project, role, start, end, description):
        self.id = str(uuid.uuid4())
        self.person = person
        self.project = project
        self.role = role
        self.start = start
        self.end = end
        self.description = description

        # Link both ways
        person.add_contribution(self)
        project.add_contribution(self)

    def __repr__(self):
        return f"<Contribution: {self.person.name} on {self.project.title} as {self.role}>"
