def profile_to_string(profile: dict) -> str:
    projects_str = "\nProjects:\n" + "\n".join(
        f"- {p['name']} ({p['date']}): {p['description']} Impact: {p['impact']}"
        for p in profile['projects']
    )
    return (
        f"{profile['name']} is a {profile['title']} in {profile['location']} "
        f"with past roles like {', '.join(profile['past_roles'])} "
        f"and skills in {', '.join(profile['skills'])}. "
        f"{profile['bio']} "
        f"{projects_str}"
    )
