from icecream import ic

from scout.eda_report import EDAReport


def test_generate_eda_report():
    dataset_path = "test_datasets/coco5"
    report_generator = EDAReport(dataset_path=dataset_path)

    report = report_generator.generate_report()
    ic(report)
