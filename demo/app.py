import gradio as gr
 
 
def convert(temperature: str, direction: str, history: list) -> tuple:
    if temperature.strip() == "":
        return (
            "",
            gr.update(
                value="<p class='error'>Please enter a temperature value.</p>",
                visible=True,
            ),
        )
 
    try:
        value = float(temperature.replace(",", "."))
    except ValueError:
        return (
            "",
            gr.update(
                value=f"<p class='error'>'{temperature}' is not a valid number.</p>",
                visible=True,
            ),
        )
 
    # Sanity-check: absolute zero is the hard physical lower bound
    if direction == "Celsius → Fahrenheit" and value < -273.15:
        return (
            "",
            gr.update(
                value="<p class='error'>Temperature below absolute zero (−273.15 °C) is impossible.</p>",
                visible=True,
            ),
        )
    if direction == "Fahrenheit → Celsius" and value < -459.67:
        return (
            "",
            gr.update(
                value="<p class='error'>Temperature below absolute zero (−459.67 °F) is impossible.</p>",
                visible=True,
            ),
        )
 
    if direction == "Celsius → Fahrenheit":
        result = (value * 9 / 5) + 32
        result_text = f"<p class='output-result'>{result:.2f}°F</p><p class='output-origin'>{value:.2f}°C</p>"
    else:
        result = (value - 32) * 5 / 9
        result_text = f"<p class='output-result'>{result:.2f}°C</p><p class='output-origin'>{value:.2f}°F</p>"
 
    return result_text, gr.update(value="", visible=False)
 
 
with gr.Blocks(
    title="🌡️ Temperature Converter", theme=gr.themes.Monochrome(font="sans-serif")
) as demo:
    gr.Markdown("# 🌡️ Temperature Converter")
    with gr.Row():
        with gr.Column():
            temperature_input = gr.Textbox(
                label="Temperature",
                placeholder="e.g. 100  or  -40.5",
                autofocus=True,
            )
            direction_input = gr.Radio(
                choices=["Celsius → Fahrenheit", "Fahrenheit → Celsius"],
                value="Celsius → Fahrenheit",
                label="Conversion direction",
            )
            # with gr.Row():
            # convert_btn = gr.Button(
            #     "Convert",
            #     variant="primary",
            # )
 
        with gr.Column():
            result_output = gr.HTML()
            error_output = gr.HTML()
 
    convert_inputs = [temperature_input, direction_input]
    convert_outputs = [result_output, error_output]
 
    callback = (convert, convert_inputs, convert_outputs)
 
    direction_input.change(*callback)
    temperature_input.input(*callback) # everytime a key changes
    temperature_input.change(*callback) # every the input changes
 
demo.launch(
    css="""
.output-origin {
  font-size: 2rem;
  color: #ccc;
  font-weight: 800;
}
.output-result {
  font-size: 7rem;
  font-weight: 900;
  line-height: 1;
}
.error {
  background: #ce0000;
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 3rem;
  color: white;
}
"""
)
 
# import gradio as gr


# def convert_temperature(temp, choice):
#     lowest_temperature = -273.15 if choice == "Celcius -> Fahrenheit" else -459.67

#     if temp < lowest_temperature:
#         return"", gr.update(
#         value = f"Please enter a temperature value")
#     if choice == "Celcius -> Fahrenheit":
#         (temp * 9/5) + 32
#     else:
#         (temp - 32) * 5/9

# with gr.Blocks() as demo:
#     gr.Markdown("Temperature Converter")
#     with gr.Row():
#         with gr.Column(scale=2):
#             temperature = gr.Number(label="Temperature", placeholder = 42)
#             Convert_btn = gr.Button("Convert")
#             temperature_choice = gr.Radio(choices= ["Celcius -> Fahrenheit", "Fahrenheit -> Celcius"],value = "Celcius -> Fahrenheit")
#             error_output = gr.Textbox(label = "", interactive = False, visible = False, show_label = False)
        
#         with gr.Column(scale=1):
#             output = gr.Textbox(label="Result")
        
#     # Region: Event listeners / handlers
#     Convert_btn.click(fn=convert_temperature, inputs=[temperature, temperature_choice], outputs=output, api_name="Convert")

# demo.launch()