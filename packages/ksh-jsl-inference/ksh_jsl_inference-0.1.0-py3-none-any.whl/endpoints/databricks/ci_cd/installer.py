from johnsnowlabs import nlp


nlp.install(
    json_license_path="/run/secrets/license",
    browser_login=False,
    force_browser=False,
    hardware_platform="cpu",
)
