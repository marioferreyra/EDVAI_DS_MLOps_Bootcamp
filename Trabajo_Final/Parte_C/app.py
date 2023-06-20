import os
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
    "orderAmount",
    "orderState",
    "paymentMethodRegistrationFailure",
    "paymentMethodType",
    "paymentMethodProvider",
    "paymentMethodIssuer",
    "transactionFailed",
    "emailDomain",
    "emailProvider",
    "customerIPAddressSimplified",
    "sameCity",
]

THRESHOLD = 0.37
MAIN_FOLDER = os.path.dirname(__file__)

# Model
model_filepath = "../data/modelo_proyecto_final.pkl"
MODEL_PATH = os.path.join(MAIN_FOLDER, model_filepath)
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# Columnas
columns_filepath = "../data/categories_ohe_without_fraudulent.pkl"
COLUMNS_PATH = os.path.join(MAIN_FOLDER, columns_filepath)
with open(COLUMNS_PATH, 'rb') as handle:
    ohe_tr = pickle.load(handle)

# Bins - Order Amount
bins_order_filepath = "../data/saved_bins_order_amount.pkl"
BINS_ORDER_PATH = os.path.join(MAIN_FOLDER, bins_order_filepath)
with open(BINS_ORDER_PATH, 'rb') as handle:
    new_saved_bins_order = pickle.load(handle)


def predict_fraud_customer(*args):
    request_dict = {
        param_name: [param_value]
        for param_name, param_value in zip(PARAMS_NAME, args)
    }

    # Generate pandas DataFrame
    single_instance = pd.DataFrame.from_dict(request_dict)

    # Manejar puntos de corte o bins
    single_instance["orderAmount"] = single_instance["orderAmount"].astype(
        float
    )
    single_instance["orderAmount"] = pd.cut(
        single_instance['orderAmount'],
        bins=new_saved_bins_order,
        include_lowest=True,
    )

    # One hot encoding
    single_instance_ohe = pd.get_dummies(single_instance)
    single_instance_ohe = single_instance_ohe.reindex(columns=ohe_tr).fillna(0)

    # Prediction
    # prediction = model.predict(single_instance_ohe)
    # score = int(prediction[0])
    # return {"score": score}
    prediction_proba = model.predict_proba(single_instance_ohe)

    # Apply threshold
    is_fraudulent = True if prediction_proba[:, 1] >= THRESHOLD else False

    return is_fraudulent


with gr.Blocks() as demo:
    gr.Markdown(
        """
        # Prevención de Fraude 🕵️‍♀️ 🕵️‍♂️
        """
    )

    with gr.Row():
        with gr.Column():

            gr.Markdown(
                """
                ## Predecir si un cliente es fraudulento o no.
                """
            )

            order_amount_slider = gr.Slider(
                label="Order amount",
                minimum=1,
                maximum=100,
                step=1,
                randomize=True,
            )

            order_state_radio = gr.Radio(
                label="Order state",
                choices=["failed", "fulfilled", "pending"],
                value="failed",
            )

            payment_method_registration_failure_radio = gr.Radio(
                label="Payment method registration failure",
                choices=["True", "False"],
                value="True",
            )

            payment_method_type_radio = gr.Radio(
                label="Payment method type",
                choices=["apple pay", "bitcoin", "card", "paypal"],
                value="bitcoin",
            )

            payment_method_provider_dropdown = gr.Dropdown(
                label="Payment method Provider",
                choices=[
                    "American Express",
                    "Diners Club / Carte Blanche",
                    "Discover",
                    "JCB 15 digit",
                    "JCB 16 digit",
                    "Maestro",
                    "Mastercard",
                    "VISA 13 digit",
                    "VISA 16 digit",
                    "Voyager",
                ],
                multiselect=False,
                value='American Express',
            )

            payment_method_issuer_dropdown = gr.Dropdown(
                label="Payment method issuer",
                choices=[
                    "Bastion Banks",
                    "Bulwark Trust Corp.",
                    "Citizens First Banks",
                    "Fountain Financial Inc.",
                    "Grand Credit Corporation",
                    "Her Majesty Trust",
                    "His Majesty Bank Corp.",
                    "Rose Bancshares",
                    "Solace Banks",
                    "Vertex Bancorp",
                    "weird",
                ],
                multiselect=False,
                value='Bastion Banks',
            )

            transaction_failed_radio = gr.Radio(
                label="Transaction failed",
                choices=["True", "False"],
                value="False",
            )

            email_domain_radio = gr.Radio(
                label="Email domain",
                choices=["biz", "com", "info", "net", "org", "weird"],
                value="com",
            )

            email_provider_radio = gr.Radio(
                label="Email provider",
                choices=["gmail", "hotmail", "yahoo", "weird", "other"],
                value="gmail",
            )

            customer_ip_address_radio = gr.Radio(
                label="Customer IP Address",
                choices=["digits_and_letters", "only_letters"],
                value="digits_and_letters",
            )

            same_city_radio = gr.Radio(
                label="Same city",
                choices=["no", "yes", "unknown"],
                value="unknown",
            )

        with gr.Column():
            gr.Markdown(
                """
                ## Predicción
                """
            )

            label = gr.Label(label="Es Fraude?")
            predict_btn = gr.Button(value="Evaluar")
            predict_btn.click(
                predict_fraud_customer,
                inputs=[
                    order_amount_slider,
                    order_state_radio,
                    payment_method_registration_failure_radio,
                    payment_method_type_radio,
                    payment_method_provider_dropdown,
                    payment_method_issuer_dropdown,
                    transaction_failed_radio,
                    email_domain_radio,
                    email_provider_radio,
                    customer_ip_address_radio,
                    same_city_radio,
                ],
                outputs=[label],
            )

    gr.Markdown(FOOTER_HTML)


def main():
    demo.launch()


if __name__ == "__main__":
    main()
