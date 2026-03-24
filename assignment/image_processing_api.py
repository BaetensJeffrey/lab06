# import gradio as gr
# import numpy as np
# from PIL import Image, ImageFilter, ImageOps

# # --- Model & Logic Setup ---
# try:
#     import torch
#     from torchvision import models, transforms
#     _TORCH = True
# except ImportError:
#     _TORCH = False

# try:
#     import cv2
#     _CV2 = True
# except ImportError:
#     _CV2 = False

# _LABELS = None
# _MODEL  = None

# def _load_model():
#     global _MODEL, _LABELS
#     if _MODEL is None and _TORCH:
#         weights = models.ResNet50_Weights.DEFAULT
#         _MODEL  = models.resnet50(weights=weights)
#         _MODEL.eval()
#         _LABELS = weights.meta["categories"]
#     return _MODEL, _LABELS

# def to_grayscale(img):
#     return ImageOps.grayscale(img).convert("RGB"), "✅ Converted to grayscale."

# def image_details(img):
#     w, h = img.size
#     arr  = np.array(img)
#     mean = arr.mean(axis=(0, 1))
#     std  = arr.std(axis=(0, 1))
#     if len(mean) == 3:
#         stats = (
#             f"R mean={mean[0]:.1f} σ={std[0]:.1f}\n"
#             f"G mean={mean[1]:.1f} σ={std[1]:.1f}\n"
#             f"B mean={mean[2]:.1f} σ={std[2]:.1f}"
#         )
#     else:
#         stats = f"Intensity mean={mean[0]:.1f} σ={std[0]:.1f}"
#     text = (
#         f"📐 Size      : {w} × {h} px\n"
#         f"🎨 Mode      : {img.mode}\n"
#         f"📊 Channels  : {arr.shape[2] if arr.ndim==3 else 1}\n"
#         f"💾 Est. size : {w*h*(arr.shape[2] if arr.ndim==3 else 1) // 1024} KB (raw)\n\n"
#         f"📈 Channel statistics\n{stats}"
#     )
#     return img, text

# def edge_detection(img):
#     if _CV2:
#         arr   = np.array(img.convert("L"))
#         edges = cv2.Canny(arr, threshold1=50, threshold2=150)
#         return Image.fromarray(edges).convert("RGB"), "✅ Edge detection via OpenCV Canny."
#     result = img.convert("L").filter(ImageFilter.FIND_EDGES).convert("RGB")
#     return result, "✅ Edge detection via PIL (install opencv-python for better results)."

# def object_recognition(img):
#     if not _TORCH:
#         return img, "⚠️ PyTorch not installed. Run:\n  pip install torch torchvision"
#     model, labels = _load_model()
#     preprocess = transforms.Compose([
#         transforms.Resize(256),
#         transforms.CenterCrop(224),
#         transforms.ToTensor(),
#         transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
#     ])
#     tensor = preprocess(img.convert("RGB")).unsqueeze(0)
#     with torch.no_grad():
#         prob = torch.nn.functional.softmax(model(tensor)[0], dim=0)
#     top5  = torch.topk(prob, 5)
#     lines = [
#         f"{labels[idx]:30s} {score.item()*100:5.1f}%  {'█' * int(score.item() * 30)}"
#         for score, idx in zip(top5.values, top5.indices)
#     ]
#     return img, "🔍 Top-5 predictions (ResNet-50):\n\n" + "\n".join(lines)

# PROCESS_OPTIONS = [
#     "Grayscale Conversion",
#     "Image Details / Statistics",
#     "Edge Detection",
#     "Object Recognition (ResNet-50)",
# ]

# def process_image(img, operation):
#     if img is None:
#         return None, "⚠️ Please upload an image first."
#     pil = Image.fromarray(img) if isinstance(img, np.ndarray) else img
#     ops = {
#         "Grayscale Conversion":           to_grayscale,
#         "Image Details / Statistics":      image_details,
#         "Edge Detection":                  edge_detection,
#         "Object Recognition (ResNet-50)": object_recognition,
#     }
#     return ops.get(operation, lambda i: (i, "Unknown operation."))(pil)

# # --- UI Styling ---

# CSS = """
# *, *::before, *::after { box-sizing: border-box; }
# body, .gradio-container { background: #ffffff !important; }

# /* Birds Viewer Styled Header */
# #app-header { 
#     padding: 24px 20px 0px 20px; 
#     background: #ffffff; 
# }
# #app-header h1 { 
#     font-size: 1.45rem !important; 
#     font-weight: 800 !important; 
#     color: #111827 !important; 
#     margin: 0 0 4px 0 !important; 
#     display: flex; 
#     align-items: center; 
#     gap: 10px; 
# }
# #app-header p { 
#     font-size: 1rem !important; 
#     font-weight: 700 !important; 
#     color: #111827 !important; 
#     margin: 0 0 12px 0 !important; 
# }
# #app-header code { 
#     font-family: monospace !important; 
#     background-color: #f3f4f6; 
#     padding: 2px 5px; 
#     border-radius: 4px; 
#     font-size: 0.85rem !important; 
#     font-weight: 400; 
#     color: #374151; 
# }

# #main-content { padding: 4px 20px 24px 20px; }
# .box { 
#     background: #ffffff !important; 
#     border: 1px solid #e5e7eb !important; 
#     border-radius: 8px !important; 
#     padding: 16px !important; 
# }

# /* Header Labels - Unified Bold Style */
# .section-header { 
#     font-size: 0.85rem !important; 
#     font-weight: 700 !important; 
#     color: #111827 !important; 
#     margin-bottom: 12px !important; 
#     display: block !important;
# }

# /* Tab Navigation Styling */
# .tab-nav {
#     border-bottom: 1px solid #e5e7eb !important;
#     background: transparent !important;
#     margin-bottom: 12px !important;
#     display: flex !important;
#     gap: 12px !important;
# }
# .tab-nav button {
#     background: transparent !important;
#     border: none !important;
#     border-bottom: 2px solid transparent !important;
#     color: #6b7280 !important;
#     font-weight: 600 !important;
#     font-size: 0.85rem !important;
#     padding: 6px 14px 10px !important;
#     border-radius: 0 !important;
#     margin: 0 !important;
# }
# .tab-nav button.selected {
#     color: #3b82f6 !important;
#     border-bottom: 2px solid #3b82f6 !important;
# }

# #process-btn, #process-btn button { 
#     background: #3b82f6 !important; 
#     color: #ffffff !important; 
#     font-weight: 600 !important; 
#     border-radius: 6px !important; 
#     padding: 12px !important; 
#     width: 100% !important; 
#     border: none !important; 
#     margin-top: 10px; 
#     cursor: pointer; 
# }

# footer, .gradio-footer { display: none !important; }
# """

# with gr.Blocks(title="🌇 Image Processing", css=CSS) as demo:
#     # Header Section
#     gr.HTML("""
#     <div id="app-header">
#         <h1>🌇 Image Processing</h1>
#         <p>Live data from the Processing Engine at <code>http://127.0.0.1:7860</code></p>
#     </div>
#     """)

#     with gr.Column(elem_id="main-content"):
#         with gr.Row(equal_height=True):
#             # Left Column
#             with gr.Column(scale=5, elem_classes="box"):
#                 gr.HTML('<p class="section-header">Input Image</p>')
                
#                 with gr.Tabs() as input_tabs:
#                     with gr.Tab("Upload", id=0):
#                         upload_img = gr.Image(type="pil", sources=["upload"], height=240, show_label=False)
#                     with gr.Tab("Webcam", id=1):
#                         webcam_img = gr.Image(type="pil", sources=["webcam"], height=240, show_label=False)
#                     with gr.Tab("Clipboard", id=2):
#                         clipboard_img = gr.Image(type="pil", sources=["clipboard"], height=240, show_label=False)

#                 gr.HTML('<p style="font-size:.85rem; font-weight:700; color:#111827; margin:16px 0 6px 0">Operation</p>')
#                 operation = gr.Dropdown(choices=PROCESS_OPTIONS, value=PROCESS_OPTIONS[0], show_label=False)

#             # Right Column
#             with gr.Column(scale=5, elem_classes="box"):
#                 gr.HTML('<p class="section-header">Result</p>')
#                 output_img  = gr.Image(height=240, interactive=False, show_label=False)
                
#                 gr.HTML('<p style="font-size:.85rem; font-weight:700; color:#111827; margin:16px 0 4px 0">Details / Info</p>')
#                 output_text = gr.Textbox(show_label=False, lines=6, interactive=False)

#         process_btn = gr.Button("Process Image", elem_id="process-btn")

#     def dispatch(upload, webcam, clipboard, op):
#         img = upload or webcam or clipboard
#         return process_image(img, op)

#     process_btn.click(
#         fn=dispatch,
#         inputs=[upload_img, webcam_img, clipboard_img, operation],
#         outputs=[output_img, output_text],
#     )

# if __name__ == "__main__":
#     demo.launch()





import gradio as gr
import numpy as np
from PIL import Image, ImageFilter, ImageOps

try:
    import torch
    from torchvision import models, transforms
    _TORCH = True
except ImportError:
    _TORCH = False

try:
    import cv2
    _CV2 = True
except ImportError:
    _CV2 = False

_LABELS = None
_MODEL  = None

def _load_model():
    global _MODEL, _LABELS
    if _MODEL is None and _TORCH:
        weights = models.ResNet50_Weights.DEFAULT
        _MODEL  = models.resnet50(weights=weights)
        _MODEL.eval()
        _LABELS = weights.meta["categories"]
    return _MODEL, _LABELS

def to_grayscale(img):
    return ImageOps.grayscale(img).convert("RGB"), "✅ Converted to grayscale."

def image_details(img):
    w, h = img.size
    arr  = np.array(img)
    mean = arr.mean(axis=(0, 1))
    std  = arr.std(axis=(0, 1))
    if len(mean) == 3:
        stats = (
            f"R mean={mean[0]:.1f} σ={std[0]:.1f}\n"
            f"G mean={mean[1]:.1f} σ={std[1]:.1f}\n"
            f"B mean={mean[2]:.1f} σ={std[2]:.1f}"
        )
    else:
        stats = f"Intensity mean={mean[0]:.1f} σ={std[0]:.1f}"
    text = (
        f"📐 Size      : {w} × {h} px\n"
        f"🎨 Mode      : {img.mode}\n"
        f"📊 Channels  : {arr.shape[2] if arr.ndim==3 else 1}\n"
        f"💾 Est. size : {w*h*(arr.shape[2] if arr.ndim==3 else 1) // 1024} KB (raw)\n\n"
        f"📈 Channel statistics\n{stats}"
    )
    return img, text

def edge_detection(img):
    if _CV2:
        arr   = np.array(img.convert("L"))
        edges = cv2.Canny(arr, threshold1=50, threshold2=150)
        return Image.fromarray(edges).convert("RGB"), "✅ Edge detection via OpenCV Canny."
    result = img.convert("L").filter(ImageFilter.FIND_EDGES).convert("RGB")
    return result, "✅ Edge detection via PIL (install opencv-python for better results)."

def object_recognition(img):
    if not _TORCH:
        return img, "⚠️ PyTorch not installed. Run:\n  pip install torch torchvision"
    model, labels = _load_model()
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    tensor = preprocess(img.convert("RGB")).unsqueeze(0)
    with torch.no_grad():
        prob = torch.nn.functional.softmax(model(tensor)[0], dim=0)
    top5  = torch.topk(prob, 5)
    lines = [
        f"{labels[idx]:30s} {score.item()*100:5.1f}%  {'█' * int(score.item() * 30)}"
        for score, idx in zip(top5.values, top5.indices)
    ]
    return img, "🔍 Top-5 predictions (ResNet-50):\n\n" + "\n".join(lines)

PROCESS_OPTIONS = [
    "Grayscale Conversion",
    "Image Details / Statistics",
    "Edge Detection",
    "Object Recognition (ResNet-50)",
]

def process_image(img, operation):
    if img is None:
        return None, "⚠️ Please upload an image first."
    pil = Image.fromarray(img) if isinstance(img, np.ndarray) else img
    ops = {
        "Grayscale Conversion":           to_grayscale,
        "Image Details / Statistics":     image_details,
        "Edge Detection":                 edge_detection,
        "Object Recognition (ResNet-50)": object_recognition,
    }
    return ops.get(operation, lambda i: (i, "Unknown operation."))(pil)

CSS = """
*, *::before, *::after { box-sizing: border-box; }

body, .gradio-container, .gradio-container * {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    font-size: 14px !important;
    color: #111827 !important;
}

body, .gradio-container {
    background: #ffffff !important;
    padding: 0 !important;
    margin: 0 !important;
}

.gradio-container > .main { padding: 0 !important; }
.contain { padding: 0 !important; }
.gap { gap: 0 !important; }

#app-header {
    padding: 14px 20px 6px 20px;
    background: #ffffff;
    border-bottom: 1px solid #e5e7eb;
}
#app-header h1 {
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    color: #111827 !important;
    margin: 0 0 2px 0;
    display: flex;
    align-items: center;
    gap: 6px;
}
#app-header p {
    font-size: .82rem !important;
    color: #6b7280 !important;
    margin: 0 0 10px 0;
}
#app-header .nav-tabs {
    display: flex;
    gap: 0;
    margin: 0;
    padding: 0;
    list-style: none;
}
#app-header .nav-tabs a {
    display: inline-block;
    padding: 6px 14px 8px;
    font-size: .85rem !important;
    color: #6b7280 !important;
    text-decoration: none;
    border-bottom: 2px solid transparent;
    margin-bottom: -1px;
}
#app-header .nav-tabs a.active {
    color: #3b82f6 !important;
    border-bottom: 2px solid #3b82f6;
    font-weight: 600 !important;
}

#main-content {
    padding: 16px 20px;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.box {
    background: #ffffff !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 6px !important;
    padding: 12px !important;
}

.gradio-image, .gradio-image > div {
    border-radius: 4px !important;
    background: #f9fafb !important;
    border: 1px solid #e5e7eb !important;
}

select {
    background: #ffffff !important;
    color: #111827 !important;
    border: 1px solid #d1d5db !important;
    border-radius: 4px !important;
    font-size: .88rem !important;
    padding: 5px 8px !important;
    width: 100% !important;
}

textarea {
    background: #ffffff !important;
    color: #111827 !important;
    font-size: .85rem !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 4px !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

#process-btn,
#process-btn button,
#process-btn span,
#process-btn button span {
    background: #3b82f6 !important;
    background-color: #3b82f6 !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: .9rem !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 11px !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: background .15s !important;
    margin-top: 8px !important;
    box-shadow: none !important;
    filter: none !important;
}
#process-btn:hover,
#process-btn button:hover,
#process-btn button:hover span {
    background: #2563eb !important;
    background-color: #2563eb !important;
}

label > span, label span {
    font-size: .8rem !important;
    font-weight: 500 !important;
    color: #374151 !important;
}

.tabs > .tab-nav {
    border-bottom: 1px solid #e5e7eb !important;
    background: transparent !important;
    padding: 0 !important;
    margin-bottom: 8px !important;
    gap: 0 !important;
}
.tabs > .tab-nav button {
    font-size: .85rem !important;
    font-weight: 500 !important;
    color: #6b7280 !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    padding: 6px 14px 8px !important;
    border-radius: 0 !important;
    margin: 0 !important;
    margin-bottom: -1px !important;
}
.tabs > .tab-nav button:hover { color: #3b82f6 !important; }
.tabs > .tab-nav button.selected {
    color: #3b82f6 !important;
    border-bottom: 2px solid #3b82f6 !important;
    font-weight: 600 !important;
}
.tabs > div[role="tabpanel"] { border: none !important; padding: 0 !important; }

footer, .gradio-footer, [class*="footer"], [class*="Footer"],
.built-with, [class*="built-with"], [class*="BuiltWith"],
[class*="api-docs"], [class*="show-api"], [class*="share-button"] {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    overflow: hidden !important;
    pointer-events: none !important;
}

#main-content > .tabs, #main-content > .tab-nav,
.gradio-container > .tabs, .gradio-container > div > .tabs,
.gradio-container .tabs > .tab-nav, .contain > .tabs > .tab-nav,
.gap > .tabs > .tab-nav, div.tabs:first-child > .tab-nav,
input[type="radio"], input[type="radio"] + label, input[type="radio"] ~ label {
    display: none !important;
}
div.tabs:first-child > div[role="tabpanel"] {
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
}
"""

JS = """
function() {
    const hide = () => {
        document.querySelectorAll('.tab-nav').forEach(nav => {
            const btns = nav.querySelectorAll('button');
            if (btns.length === 1 && btns[0].textContent.trim() === 'Process') {
                nav.style.display = 'none';
            }
        });
    };
    hide();
    setTimeout(hide, 300);
    setTimeout(hide, 1000);
}
"""

with gr.Blocks(title="🌇 Image Processing", css=CSS, js=JS) as demo:

    gr.HTML("""
    <div id="app-header">
        <h1>🌇 Image Processing</h1>
        <p>Upload an image, select an operation, and click <strong>Process Image</strong>.</p>
    """)

    with gr.Column(elem_id="main-content"):
        with gr.Row(equal_height=True, variant="panel"):

            with gr.Column(scale=5, elem_classes="box"):
                gr.HTML('<p style="font-size:.82rem;font-weight:600;color:#111827;margin:0 0 4px 0">Input Image</p>')
                with gr.Tabs():
                    with gr.Tab("Upload"):
                        upload_img = gr.Image(type="pil", sources=["upload"], height=220, show_label=False)
                    with gr.Tab("Webcam"):
                        webcam_img = gr.Image(type="pil", sources=["webcam"], height=220, show_label=False)
                    with gr.Tab("Clipboard"):
                        clipboard_img = gr.Image(type="pil", sources=["clipboard"], height=220, show_label=False)

                gr.HTML('<p style="font-size:.82rem;font-weight:600;color:#111827;margin:12px 0 4px 0">Operation</p>')
                operation = gr.Dropdown(
                    choices=PROCESS_OPTIONS,
                    value=PROCESS_OPTIONS[0],
                    label="Select what to do with the image",
                    interactive=True,
                )

            with gr.Column(scale=5, elem_classes="box"):
                gr.HTML('<p style="font-size:.82rem;font-weight:600;color:#111827;margin:0 0 4px 0">Result</p>')
                output_img  = gr.Image(label="Processed Image", height=220, interactive=False)
                gr.HTML('<p style="font-size:.82rem;font-weight:600;color:#111827;margin:12px 0 4px 0">Details / Info</p>')
                output_text = gr.Textbox(show_label=False, lines=5, interactive=False)

        process_btn = gr.Button("Process Image", elem_id="process-btn")

    def dispatch(upload, webcam, clipboard, op):
        return process_image(upload or webcam or clipboard, op)

    process_btn.click(
        fn=dispatch,
        inputs=[upload_img, webcam_img, clipboard_img, operation],
        outputs=[output_img, output_text],
    )

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Default(primary_hue="blue"))
