import math
from resume.career_data import ROLE_SKILL_MAP, get_resource_for_skill, get_roadmap_url, get_topics


def _build_skill_node(skill, status):
    res = get_resource_for_skill(skill)
    return {
        "skill": skill,
        "resource": res["resource"],
        "weeks": res["weeks"],
        "category": res["category"],
        "roadmap_url": get_roadmap_url(skill),
        "topics": get_topics(skill),
        "status": status,  # "Done" | "Not Started" | "Learning" | "Skip"
    }


def generate_roadmap(current_skills, target_role):
    """
    Build a click-through skill tree to go from `current_skills` to being
    job-ready for `target_role`. Every skill (matched or missing) becomes a
    node with a status and a topic breakdown for the detail panel.
    """
    current_skills_lower = set(s.lower() for s in current_skills)
    required_skills = ROLE_SKILL_MAP.get(target_role, [])

    matched = [s for s in required_skills if s in current_skills_lower]
    missing = [s for s in required_skills if s not in current_skills_lower]

    readiness = int((len(matched) / len(required_skills)) * 100) if required_skills else 0

    phases = []

    if matched:
        phases.append({
            "phase": "Already Have",
            "description": "Skills you already know for this role.",
            "skills": [_build_skill_node(s, "Done") for s in matched],
            "estimated_weeks": 0,
        })

    phases_config = [
        ("Foundation (0-2 months)", "Get comfortable with the core building blocks."),
        ("Intermediate (2-4 months)", "Build real projects and go deeper on the stack."),
        ("Specialization (4-6 months)", "Round out with deployment, scale, and advanced tools."),
    ]

    if missing:
        chunk_size = math.ceil(len(missing) / len(phases_config))
        for i, (phase_name, phase_desc) in enumerate(phases_config):
            chunk = missing[i * chunk_size: (i + 1) * chunk_size]
            if not chunk:
                continue
            skill_entries = [_build_skill_node(s, "Not Started") for s in chunk]
            total_weeks = sum(s["weeks"] for s in skill_entries)
            phases.append({
                "phase": phase_name,
                "description": phase_desc,
                "skills": skill_entries,
                "estimated_weeks": total_weeks,
            })

    total_weeks = sum(
        p["estimated_weeks"] for p in phases if p["phase"] != "Already Have"
    )

    return {
        "target_role": target_role,
        "readiness_percent": readiness,
        "matched_skills": matched,
        "missing_skills": missing,
        "phases": phases,
        "total_estimated_weeks": total_weeks,
    }


def generate_roadmaps_for_roles(current_skills, target_roles):
    """Convenience wrapper: build a roadmap for each role in a list."""
    return [generate_roadmap(current_skills, role) for role in target_roles]