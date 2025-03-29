from IPython.display import HTML, display
def set_output_wrapping():
    display(HTML('''
    <style>
    pre {
        white-space: pre-wrap;
        word-wrap: break-word;
        max-width: 100%;
        overflow-x: hidden;
    }
    .output_area {
        white-space: pre-wrap;
        word-wrap: break-word;
        max-width: 100%;
        overflow-x: hidden;
    }
    .output_text {
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    div.output {
        white-space: pre-wrap;
        word-wrap: break-word;
        max-width: 100%;
    }
    span {
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    </style>
    '''))
    