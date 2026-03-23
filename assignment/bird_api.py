import gradio as gr
import httpx
import pandas as pd

# API Base URL based on your screenshot
BASE_URL = "http://127.0.0.1:8000/species"

def fetch_bird_data(filter_status="All"):
    try:
        r = httpx.get(BASE_URL)
        r.raise_for_status()
        data = r.json()
        
        df = pd.DataFrame(data)
        
        # Apply filter if not "All"
        if filter_status and filter_status != "All":
            df = df[df['conservation_status'] == filter_status]
            
        return df
    except Exception as e:
        # Returns an empty dataframe with correct headers if API is down
        return pd.DataFrame(columns=["id", "name", "scientific_name", "family", "conservation_status", "wingspan_cm"])

def create_species(name, sci_name, family, status, wingspan):
    payload = {
        "name": name,
        "scientific_name": sci_name,
        "family": family,
        "conservation_status": status,
        "wingspan_cm": wingspan
    }
    try:
        r = httpx.post(BASE_URL, json=payload)
        r.raise_for_status()
        return fetch_bird_data() # Refresh table after adding
    except Exception as e:
        return fetch_bird_data()

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🐦 Birds Viewer")
    gr.Markdown(f"Live data from the Birds API at `{BASE_URL}`")

    with gr.Tab("Species"):
        with gr.Row():
            status_filter = gr.Dropdown(
                choices=[
                        "Least Concern",
                        "Near Threatened",
                        "Vulnerable",
                        "Endangered",
                        "Critically Endangered",
                        "Extinct in the Wild",
                        "Extinct"
                    ],  
                value="All", 
                label="Filter by conservation status", 
                scale=4
            )
            refresh_button = gr.Button("🔄 Refresh", scale=1)

        bird_df = gr.Dataframe(
            value=fetch_bird_data,
            headers=["id", "name", "scientific_name", "family", "conservation_status", "wingspan_cm"],
            interactive=False
        )

        with gr.Accordion("➕ Add new species", open=True):
            with gr.Row():
                name_input = gr.Textbox(label="Name", placeholder="e.g. Atlantic Puffin")
                sci_input = gr.Textbox(label="Scientific name", placeholder="e.g. Fratercula arctica")
            
            with gr.Row():
                family_input = gr.Textbox(label="Family", placeholder="e.g. Alcidae")
                status_input = gr.Dropdown(
                    choices=[
                        "Least Concern",
                        "Near Threatened",
                        "Vulnerable",
                        "Endangered",
                        "Critically Endangered",
                        "Extinct in the Wild",
                        "Extinct"
                    ], 
                    label="Conservation status", 
                    value="LC"
                )
                wingspan_input = gr.Slider(
                    label="Wingspan (cm)", 
                    minimum=0, 
                    maximum=300, 
                    value=155, 
                    step=1
                )
            
            create_btn = gr.Button("Create species", variant="primary")

    # Event Listeners
    refresh_button.click(fn=fetch_bird_data, inputs=[status_filter], outputs=[bird_df])
    status_filter.change(fn=fetch_bird_data, inputs=[status_filter], outputs=[bird_df])
    
    create_btn.click(
        fn=create_species, 
        inputs=[name_input, sci_input, family_input, status_input, wingspan_input],
        outputs=[bird_df]
    )

if __name__ == "__main__":
    demo.launch()
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
            
        
