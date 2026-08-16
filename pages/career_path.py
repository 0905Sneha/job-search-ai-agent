import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from style import apply_custom_style
from database import (
    init_db, save_roadmap, get_roadmaps, update_roadmap_status,
    delete_roadmap, update_skill_status, compute_completion_percent
)
from resume.career_data import get_all_roles
from resume.roadmap import generate_roadmap

init_db()

st.set_page_config(page_title="Career Path", page_icon="🧭", layout="wide")
apply_custom_style()

STATUS_EMOJI = {"Done": "✅", "Learning": "📖", "Skip": "⏭️", "Not Started": "⚪"}
STATUS_COLOR = {
    "Done": "#1D9E75",         # green
    "Learning": "#EF9F27",     # amber
    "Skip": "#5F5E5A",         # muted gray
    "Not Started": "#7c83fd",  # indigo (default accent)
}
PHASE_COLOR = "#22d3ee"
ROOT_COLOR = "#7c83fd"


def set_status(skill_name, new_status):
    roadmap = st.session_state.get("career_roadmap")
    if not roadmap:
        return
    for phase in roadmap["phases"]:
        for s in phase["skills"]:
            if s["skill"] == skill_name:
                s["status"] = new_status


def find_skill_node(roadmap, skill_name):
    for phase in roadmap["phases"]:
        for s in phase["skills"]:
            if s["skill"] == skill_name:
                return s
    return None


def build_graph(roadmap):
    """Turn the phases/skills into a top-down node tree with connector edges."""
    nodes = [Node(id="root", label=roadmap["target_role"], size=28,
                   color=ROOT_COLOR, shape="box", font={"color": "#ffffff", "size": 16})]
    edges = []
    prev_phase_id = "root"

    for phase in roadmap["phases"]:
        phase_id = f"phase::{phase['phase']}"
        nodes.append(Node(id=phase_id, label=phase["phase"], size=22,
                           color=PHASE_COLOR, shape="box", font={"color": "#0a0c1a", "size": 13}))
        edges.append(Edge(source=prev_phase_id, target=phase_id))

        for skill in phase["skills"]:
            skill_id = f"skill::{skill['skill']}"
            color = STATUS_COLOR.get(skill.get("status", "Not Started"), "#7c83fd")
            label = f"{STATUS_EMOJI.get(skill.get('status'), '⚪')} {skill['skill'].title()}"
            nodes.append(Node(id=skill_id, label=label, size=16,
                               color=color, shape="box", font={"color": "#ffffff", "size": 12}))
            edges.append(Edge(source=phase_id, target=skill_id))

        prev_phase_id = phase_id

    return nodes, edges


st.title("Career Path Recommendations")
st.caption("Pick a target role, click any node in the tree, and see exactly what to learn.")

current_skills = []
suggested_roles = []
if "parsed_resume" in st.session_state:
    current_skills = st.session_state["parsed_resume"].get("skills", [])
if "resume_analysis" in st.session_state:
    suggested_roles = st.session_state["resume_analysis"].get("recommended_roles", [])

if not current_skills:
    st.info("No resume on file yet — you can still explore a roadmap, but for a personalized skill "
             "gap analysis, upload your resume on the **Resume Parser** page first.")

all_roles = get_all_roles()
ordered_roles = [r for r in suggested_roles if r in all_roles] + [r for r in all_roles if r not in suggested_roles]

col_a, col_b = st.columns([3, 1])
with col_a:
    target_role = st.selectbox(
        "Target role", ordered_roles, index=None, placeholder="Select a target role..."
    )
with col_b:
    st.write("")
    st.write("")
    generate_clicked = st.button("Generate Roadmap", use_container_width=True, disabled=(target_role is None))

if generate_clicked and target_role:
    st.session_state["career_roadmap"] = generate_roadmap(current_skills, target_role)
    st.session_state["selected_skill"] = None

if "career_roadmap" in st.session_state:
    roadmap = st.session_state["career_roadmap"]
    fully_matched = not roadmap["missing_skills"]

    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown(f'<div class="stat-box"><div class="stat-number">{roadmap["readiness_percent"]}%</div><div class="stat-label">Job-Ready Today</div></div>', unsafe_allow_html=True)
    with s2:
        st.markdown(f'<div class="stat-box"><div class="stat-number">{len(roadmap["missing_skills"])}</div><div class="stat-label">Skills To Learn</div></div>', unsafe_allow_html=True)
    with s3:
        st.markdown(f'<div class="stat-box"><div class="stat-number">{roadmap["total_estimated_weeks"]}w</div><div class="stat-label">Estimated Timeline</div></div>', unsafe_allow_html=True)

    st.write("")

    if fully_matched:
        st.success("You already cover every core skill typically expected for this role — "
                    "nothing left to learn here. Focus on projects and interview prep next!")

    st.subheader(" Skill Tree")
    st.caption("🟣 role · 🔵 phase · nodes below colored by status: ⚪ not started · 📖 learning · ✅ done · ⏭️ skip")

    tree_col, detail_col = st.columns([2, 1])

    with tree_col:
        nodes, edges = build_graph(roadmap)
        config = Config(
            width="100%",
            height=520,
            directed=True,
            physics=False,
            hierarchical=True,
            hierarchical_sort_method="directed",
            nodeHighlightBehavior=True,
            highlightColor="#22d3ee",
        )
        clicked_id = agraph(nodes=nodes, edges=edges, config=config)
        if clicked_id and clicked_id.startswith("skill::"):
            st.session_state["selected_skill"] = clicked_id[len("skill::"):]

    with detail_col:
        selected = st.session_state.get("selected_skill")
        if not selected:
            st.info("Click any skill node in the tree to see its detailed topic list here.")
        else:
            skill_node = find_skill_node(roadmap, selected)
            if skill_node:
                st.markdown(f"### {skill_node['skill'].title()}")

                btn1, btn2, btn3 = st.columns(3)
                with btn1:
                    if st.button("Learning", key="mark_learning", use_container_width=True):
                        set_status(selected, "Learning")
                        st.rerun()
                with btn2:
                    if st.button("Done", key="mark_done", use_container_width=True):
                        set_status(selected, "Done")
                        st.rerun()
                with btn3:
                    if st.button("⏭Skip", key="mark_skip", use_container_width=True):
                        set_status(selected, "Skip")
                        st.rerun()

                st.caption(f"Current status: **{skill_node.get('status', 'Not Started')}**")
                st.divider()

                for section in skill_node["topics"]:
                    st.markdown(f"**{section['heading']}**")
                    for point in section["points"]:
                        st.write(f"- {point}")
                    st.write("")

                st.caption(f"Suggested resource: {skill_node['resource']} (~{skill_node['weeks']} weeks)")

    if fully_matched:
        st.caption("No roadmap to save — you're already 100% matched on core skills for this role.")
    else:
        if st.button("💾 Save this roadmap"):
            save_roadmap(roadmap)
            st.success(f"Roadmap for {roadmap['target_role']} saved!")

st.divider()

st.subheader(" My Saved Roadmaps")
saved = get_roadmaps()
if not saved:
    st.info("No roadmaps saved yet.")
else:
    status_options_list = ["Not Started", "In Progress", "Completed"]
    for item in saved:
        progress_pct = compute_completion_percent(item["roadmap"])
        st.markdown(f"""
            <div class="job-card">
                <h4>{item['target_role']}</h4>
                <div class="job-meta">Readiness at save time: {item['readiness_percent']}% &nbsp;|&nbsp; Saved: {item['saved_at']}</div>
            </div>
        """, unsafe_allow_html=True)
        st.progress(progress_pct / 100, text=f"{progress_pct}% of skills marked Done")

        with st.expander("View skill tree & update progress"):
            for phase in item["roadmap"].get("phases", []):
                st.write(f"**{phase['phase']}**")
                for skill in phase["skills"]:
                    current_status = skill.get("status", "Not Started")
                    new_status = st.selectbox(
                        skill["skill"].title(),
                        ["Not Started", "Learning", "Done", "Skip"],
                        index=["Not Started", "Learning", "Done", "Skip"].index(current_status),
                        key=f"saved_{item['id']}_{skill['skill']}_status"
                    )
                    if new_status != current_status:
                        update_skill_status(item["id"], skill["skill"], new_status)
                        st.rerun()

        col1, col2 = st.columns([2, 1])
        with col1:
            new_roadmap_status = st.selectbox(
                "Overall status", status_options_list, index=status_options_list.index(item["status"]),
                key=f"roadmap_status_{item['id']}"
            )
            if new_roadmap_status != item["status"]:
                update_roadmap_status(item["id"], new_roadmap_status)
                st.rerun()
        with col2:
            if st.button("Remove", key=f"del_roadmap_{item['id']}"):
                delete_roadmap(item["id"])
                st.rerun()