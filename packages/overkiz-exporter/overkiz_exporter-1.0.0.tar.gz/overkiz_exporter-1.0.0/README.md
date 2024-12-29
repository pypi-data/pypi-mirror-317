![PyPI - Version](https://img.shields.io/pypi/v/overkiz-exporter) ![Docker Image Version](https://img.shields.io/docker/v/jaesivsm/overkiz-exporter)

# Overkiz Exporter

A simple open metrics exporter for metrics yielded from overkiz api.

## Metrics served

* `overkiz_exporter`: Will serve various metrics about the exporter itself.
* `overkiz_measurable`: Will export any float or integer value returned by the overkiz API and tag it with the device specifics.
* `overkiz_label`: Will export any string values returned by the overkiz API. The string value will be placed in the `label` label and the value set to `1`.

## Used labels

| Label              | Available on                          | Comment                                                                                  |
|--------------------|---------------------------------------|------------------------------------------------------------------------------------------|
| `status`           | `overkiz_exporter`                    | Any value, describe the runtime status of the exporter                                   |
| `device_id`        | `overkiz_measurable`, `overkiz_label` | The device id of the current metric                                                      |
| `device_label`     | `overkiz_measurable`, `overkiz_label` | The device name, may be customized                                                       |
| `metric_namespace` | `overkiz_measurable`, `overkiz_label` | The metric namespace, extracted from the API name (example: `core`, `modbuslink`)        |
| `metric_name`      | `overkiz_measurable`, `overkiz_label` | The metric name, extracted from the API name (example: `NameState`, `NumberOfTankState`) |
| `label`            | `overkiz_measurable`                  | The value outputed by the API (example: `Heating`, `off)                                 |

## Example configuration

```json
{
    "credentials": [
        {
            "username": "<login to your atlantic account>",
            "password": "<password to your atlantic account>",
            "servertype": "ATLANTIC_COZYTOUCH"
        }
    ]
}
```

## Running it

For the next few bits of code, we'll suppose you have a working configuration above in `~/.config/overkiz_exporter.json`.


... with python:

```shell
pip install overkiz-exporter
python -m overkiz_exporter
```

... with docker

```shell
 docker run -v /home/jaes/.config/:/etc/overkiz-exporter/:ro -p 8500:8500 overkiz-exporter:main
```

You'll then be able retrieve some values:

```shell
curl localhost:8500/metrics

# HELP overkiz_exporter
# TYPE overkiz_exporter gauge
overkiz_exporter{status="loop_interval"} 60.0
overkiz_exporter{status="credentials_count"} 1.0
overkiz_exporter{status="ok"} 1.0
overkiz_exporter{status="nok"} 0.0
[...]
```
