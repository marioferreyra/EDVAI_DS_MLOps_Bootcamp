import pickle
import pandas as pd
import gradio as gr


EDVAI_URL = """\
https://www.escueladedatosvivos.ai/cursos/bootcamp-de-data-science
"""
FOOTER_HTML = f"""\
<p style='text-align: center'>
    <a href='{EDVAI_URL}' target='_blank'>
        Proyecto demo creado en el bootcamp de EDVAI 🤗
    </a>
</p>
"""

# Define params names
PARAMS_NAME = [
    "Age",
    "Class",
    "Wifi",
    "Booking",
    "Seat",
    "Checkin",
]

# Load model
with open("model/rf.pkl", "rb") as f:
    model = pickle.load(f)


# Columnas
COLUMNS_PATH = "pickle_files/categories_ohe.pkl"
with open(COLUMNS_PATH, 'rb') as handle:
    ohe_tr = pickle.load(handle)


def predict(*args):
    answer_dict = {
        param_name: [param_value]
        for param_name, param_value in zip(PARAMS_NAME, args)
    }

    single_instance = pd.DataFrame.from_dict(answer_dict)

    # Reformat columns
    single_instance_ohe = pd.get_dummies(single_instance)
    single_instance_ohe = single_instance_ohe.reindex(columns=ohe_tr).fillna(0)

    prediction = model.predict(single_instance_ohe)

    response = format(prediction[0], '.2f')

    return response


with gr.Blocks() as demo:
    gr.Markdown(
        """
        # Satisfacción aerolínea 🛫 🌎 🛬
        """
    )

    with gr.Row():
        with gr.Column():

            gr.Markdown(
                """
                ## ¿Cliente satisfecho?
                """
            )

            age = gr.Slider(
                label="Edad",
                minimum=1,
                maximum=100,
                step=1,
                randomize=True,
            )

            class_ = gr.Radio(
                label="Tipo de Herramienta",
                choices=["Business", "Eco", "Eco Plus"],
                value="Business",
            )

            wifi = gr.Slider(
                label="Servicio de Wifi",
                minimum=0,
                maximum=5,
                step=1,
                randomize=True,
            )

            booking = gr.Slider(
                label="Facilidad de registro",
                minimum=0,
                maximum=5,
                step=1,
                randomize=True,
            )

            seat = gr.Dropdown(
                label="Comodidad del asiento",
                choices=[0, 1, 2, 3, 4, 5],
                multiselect=False,
                value=0,
            )

            checking = gr.Dropdown(
                label="Experiencia con el Checkin",
                choices=[0, 1, 2, 3, 4, 5],
                multiselect=False,
                value=0,
            )

        with gr.Column():
            gr.Markdown(
                """
                ## Predicción
                """
            )

            label = gr.Label(label="Score")
            predict_btn = gr.Button(value="Evaluar")
            predict_btn.click(
                predict,
                inputs=[
                   age,
                   class_,
                   wifi,
                   booking,
                   seat,
                   checking,
                ],
                outputs=[label],
            )

    gr.Markdown(FOOTER_HTML)


if __name__ == "__main__":
    demo.launch()
