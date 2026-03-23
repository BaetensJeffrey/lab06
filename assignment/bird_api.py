import gradio as gr
import httpx

API_BASE = "http://127.0.0.1:8080"

conservation_statuses = [
    "All", 
    "Least Concern",
    "Near Threatened",
    "Vulnerable",
    "Endangered",
    "Critically Endangered",
    "Extinct in the Wild",
    "Extinct"
]

bird_families = [
    "Accipitridae", "Alaudidae", "Alcedinidae", "Alcidae", "Anatidae",
    "Apodidae", "Ardeidae", "Caprimulgidae", "Charadriidae", "Ciconiidae",
    "Cinclidae", "Columbidae", "Corvidae", "Cuculidae", "Emberizidae",
    "Falconidae", "Fringillidae", "Gaviidae", "Gruidae", "Hirundinidae",
    "Laridae", "Meropidae", "Motacillidae", "Muscicapidae", "Paridae",
    "Passeridae", "Phalacrocoracidae", "Picidae", "Podicipedidae",
    "Procellariidae", "Psittacidae", "Rallidae", "Regulidae", "Scolopacidae",
    "Sittidae", "Strigidae", "Sturnidae", "Sulidae", "Sylviidae",
    "Threskiornithidae", "Troglodytidae", "Turdidae", "Tytonidae", "Upupidae",
]


# Species helpers 

def fetch_bird_data(status_filter="All"):
    try:
        params = {}
        if status_filter and status_filter != "All":
            params["conservation_status"] = status_filter
        r = httpx.get(f"{API_BASE}/species", params=params, timeout=5)
        r.raise_for_status()
        data = r.json()
        if not data:
            return []
        return [[s.get("id"), s.get("name"), s.get("scientific_name"),
                 s.get("family"), s.get("conservation_status"),
                 s.get("wingspan_cm")] for s in data]
    except Exception:
        return []


def create_species(name, scientific_name, family, conservation_status, wingspan_cm):
    try:
        payload = {
            "name": name,
            "scientific_name": scientific_name,
            "family": family,
            "conservation_status": conservation_status,
            "wingspan_cm": float(wingspan_cm),
        }
        r = httpx.post(f"{API_BASE}/species", json=payload, timeout=5)
        r.raise_for_status()
        gr.Info(f"✅ Species '{name}' created successfully!")
    except Exception as e:
        gr.Warning(f"❌ Error: {e}")


def get_species_choices():
    try:
        r = httpx.get(f"{API_BASE}/species", timeout=5)
        r.raise_for_status()
        data = r.json()
        return [(f"{s.get('name')} ({s.get('scientific_name')})", s.get("id")) for s in data]
    except Exception:
        return []


# Birds helpers

def fetch_birds():
    try:
        r = httpx.get(f"{API_BASE}/birds", timeout=5)
        r.raise_for_status()
        data = r.json()
        if not data:
            return []
        return [[b.get("id"), b.get("nickname"), b.get("ring_code"),
                 b.get("age"), b.get("species")] for b in data]
    except Exception:
        return []


def create_bird(nickname, ring_code, age, species_id):
    try:
        payload = {
            "nickname": nickname,
            "ring_code": ring_code,
            "age": int(age) if age else None,
            "species_id": species_id,
        }
        r = httpx.post(f"{API_BASE}/birds", json=payload, timeout=5)
        r.raise_for_status()
        gr.Info(f"✅ Bird '{nickname}' created successfully!")
    except Exception as e:
        gr.Warning(f"❌ Error: {e}")


def get_bird_choices():
    try:
        r = httpx.get(f"{API_BASE}/birds", timeout=5)
        r.raise_for_status()
        data = r.json()
        return [(f"{b.get('nickname')} ({b.get('ring_code')})", b.get("id")) for b in data]
    except Exception:
        return []


# Sightings helpers

def fetch_sightings(observer_filter=""):
    try:
        params = {}
        if observer_filter:
            params["observer_name"] = observer_filter
        r = httpx.get(f"{API_BASE}/sightings", params=params, timeout=5)
        r.raise_for_status()
        data = r.json()
        if not data:
            return []
        return [[s.get("id"), s.get("bird"), s.get("spotted_at"),
                 s.get("location"), s.get("observer_name"),
                 s.get("notes")] for s in data]
    except Exception:
        return []


def create_sighting(bird_id, spotted_at, location, observer_name, notes):
    try:
        payload = {
            "bird_id": bird_id,
            "spotted_at": spotted_at,
            "location": location,
            "observer_name": observer_name,
            "notes": notes if notes else None,
        }
        r = httpx.post(f"{API_BASE}/sightings", json=payload, timeout=5)
        r.raise_for_status()
        gr.Info("✅ Sighting recorded successfully!")
    except Exception as e:
        gr.Warning(f"❌ Error: {e}")


# UI 

with gr.Blocks(title="Birds Viewer") as demo:
    gr.Markdown("# 🐦 Birds Viewer")
    gr.Markdown(f"Live data from the Birds API at `{API_BASE}`.")

    # Species tab
    with gr.Tab("Species"):
        with gr.Row():
            status_filter = gr.Dropdown(
                choices=conservation_statuses,
                value="All",
                label="Filter by conservation status",
                scale=2,
            )
            refresh_button = gr.Button("🔄 Refresh", scale=1)

        species_table = gr.DataFrame(
            headers=["id", "name", "scientific_name", "family",
                     "conservation_status", "wingspan_cm"],
            value=fetch_bird_data(),
            label="Species",
            interactive=False,
        )

        gr.Markdown("### ➕ Add new species")
        with gr.Row():
            name            = gr.Textbox(label="Name", placeholder="e.g. Atlantic Puffin")
            scientific_name = gr.Textbox(label="Scientific name", placeholder="e.g. Fratercula arctica")
        with gr.Row():
            family              = gr.Dropdown(choices=bird_families, label="Family", allow_custom_value=True)
            conservation_status = gr.Dropdown(choices=conservation_statuses[1:], value="Least Concern", label="Conservation status")
            wingspan_cm         = gr.Slider(label="Wingspan (cm)", minimum=5, maximum=350, step=1, value=50)
        with gr.Row():
            add_button = gr.Button("Create species", variant="primary")

        refresh_button.click(
            fn=fetch_bird_data,
            inputs=[status_filter],
            outputs=[species_table],
        )
        status_filter.change(
            fn=fetch_bird_data,
            inputs=[status_filter],
            outputs=[species_table],
        )
        add_button.click(
            fn=create_species,
            inputs=[name, scientific_name, family, conservation_status, wingspan_cm],
            outputs=[],
        ).then(
            fn=fetch_bird_data,
            inputs=[status_filter],
            outputs=[species_table],
        )

    # Birds tab
    with gr.Tab("Birds"):
        with gr.Row():
            refresh_birds_button = gr.Button("🔄 Refresh")

        birds_table = gr.DataFrame(
            headers=["id", "nickname", "ring_code", "age", "species"],
            value=fetch_birds(),
            label="Birds",
            interactive=False,
        )

        gr.Markdown("### ➕ Add new bird")
        with gr.Row():
            b_nickname = gr.Textbox(label="Nickname", placeholder="e.g. Skipper")
            b_ring     = gr.Textbox(label="Ring code", placeholder="e.g. RB-1234")
        with gr.Row():
            b_age     = gr.Number(label="Age (years)", precision=0, value=0)
            b_species = gr.Dropdown(
                choices=get_species_choices(),
                label="Species",
            )
        with gr.Row():
            refresh_species_btn = gr.Button("🔄 Refresh species list")
            add_bird_button     = gr.Button("Create bird", variant="primary")

        refresh_birds_button.click(fn=fetch_birds, outputs=[birds_table])
        refresh_species_btn.click(fn=get_species_choices, outputs=[b_species])
        add_bird_button.click(
            fn=create_bird,
            inputs=[b_nickname, b_ring, b_age, b_species],
            outputs=[],
        ).then(fn=fetch_birds, outputs=[birds_table])

    # Sightings tab
    with gr.Tab("Sightings"):
        with gr.Row():
            observer_filter          = gr.Textbox(label="Filter by observer name", placeholder="e.g. Jane", scale=2)
            refresh_sightings_button = gr.Button("🔄 Refresh", scale=1)

        sightings_table = gr.DataFrame(
            headers=["id", "bird", "spotted_at", "location", "observer_name", "notes"],
            value=fetch_sightings(),
            label="Sightings",
            interactive=False,
        )

        gr.Markdown("### ➕ Add new sighting")
        with gr.Row():
            s_bird             = gr.Dropdown(choices=get_bird_choices(), label="Bird")
            refresh_birds_list = gr.Button("🔄 Refresh bird list")
        with gr.Row():
            s_spotted_at = gr.Textbox(label="Spotted at (ISO 8601)", placeholder="e.g. 2024-06-01T09:30:00")
            s_location   = gr.Textbox(label="Location", placeholder="e.g. Cliffs of Moher")
        with gr.Row():
            s_observer = gr.Textbox(label="Observer name", placeholder="e.g. Jane Doe")
            s_notes    = gr.Textbox(label="Notes (optional)", placeholder="e.g. Flying low over the water")
        with gr.Row():
            add_sighting_button = gr.Button("Create sighting", variant="primary")

        refresh_sightings_button.click(
            fn=fetch_sightings,
            inputs=[observer_filter],
            outputs=[sightings_table],
        )
        observer_filter.change(
            fn=fetch_sightings,
            inputs=[observer_filter],
            outputs=[sightings_table],
        )
        refresh_birds_list.click(fn=get_bird_choices, outputs=[s_bird])
        add_sighting_button.click(
            fn=create_sighting,
            inputs=[s_bird, s_spotted_at, s_location, s_observer, s_notes],
            outputs=[],
        ).then(
            fn=fetch_sightings,
            inputs=[observer_filter],
            outputs=[sightings_table],
        )


if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft())
# import gradio as gr
# import httpx

# def fetch_bird_data():

#     r = httpx.get('')
#     data = r.json()
#     dataframe = pd.Dataframe(data, columns = [], )
#     return r.json()

# def create_species(name,scientific_name,family,conservation_status, wingspan_cm):

# with gr.Blocks(theme = gr.themes.Soft) as demo:
#     gr.Markdown("## Birds API assignment")

#     with gr.Tab("Species"):
#         with gr.Row():
#             gr.Dropdown(label = "Filter by conservation status", scale = 2)
#             refresh_button = gr.Button("Refresh", scale = 1)

#         with gr.Row():
#             gr.Dataframe(
#                 value = fetch_bird_data()
#                 interactive = True
#             )

#         sdfghgfdsrhgfdsgfdgfd

#         with gr.Row():
#             with gr.Row():
#                 name = gr.T(label = "Name")
#                 scientific_name =

#             with gr.Row():
#                 conservation_status = 
#                 family = 
#                 wingspan_cm = gr.Slider(label = , minimum = 5, maximum = 350, step =1)
#             with gr.Row():
#                 add_button.click(fn=)
            
        
