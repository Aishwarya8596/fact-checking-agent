import os

import gradio as gr

from session_15_structured_final_report import build_final_report


EXAMPLE_CLAIM = (
    "The Eiffel Tower is in Paris, Berlin is the capital of Germany, "
    "and Mars is known as the Red Planet."
)


def fact_check_claim(claim):
    if not claim or not claim.strip():
        return "Please enter a claim.", "", {}

    try:
        report = build_final_report(claim.strip())
    except SystemExit:
        return (
            "Setup error",
            "Check that OPENAI_API_KEY is set in the terminal running this app.",
            {},
        )
    except Exception as error:
        return "Error", str(error), {}

    final_verdict = report["final_verdict"]
    final_reason = report["final_reason"]

    return final_verdict, final_reason, report


def build_app():
    with gr.Blocks(title="Fact Checking Agent") as app:
        gr.Markdown("# Fact Checking Agent")

        claim_input = gr.Textbox(
            label="Claim",
            value=EXAMPLE_CLAIM,
            lines=4,
        )

        run_button = gr.Button("Fact Check", variant="primary")

        final_verdict = gr.Textbox(label="Final Verdict")
        final_reason = gr.Textbox(label="Final Reason", lines=2)
        report_output = gr.JSON(label="Structured Report")

        run_button.click(
            fn=fact_check_claim,
            inputs=claim_input,
            outputs=[final_verdict, final_reason, report_output],
        )

    return app


def main():
    app = build_app()
    server_port = int(os.getenv("GRADIO_SERVER_PORT", "50992"))
    app.launch(server_port=server_port)


if __name__ == "__main__":
    main()
