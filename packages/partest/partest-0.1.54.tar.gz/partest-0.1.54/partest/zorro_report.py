import allure

from partest.test_types import TypesTestCases
from partest.allure_graph import create_chart
from partest.call_storage import call_count, call_type
from confpartest import test_types_coverage, test_types_exception
from partest.parparser import SwaggerSettings
from confpartest import swagger_files

types = TypesTestCases
required_types = test_types_coverage
exception_types = test_types_exception
swagger_settings = SwaggerSettings(swagger_files)
paths_info = swagger_settings.collect_paths_info()


def zorro():
    """Function for displaying the total number of API calls and test types."""
    report_lines = []
    total_coverage_percentage = 0
    total_endpoints = 0
    total_calls_excluding_generation = 0

    # Словарь для хранения отчетов по каждому Swagger API
    swagger_reports = {}

    for (method, endpoint, description), count in call_count.items():
        # Проверка, является ли эндпоинт устаревшим
        is_deprecated = any(
            path['path'] == endpoint and path['method'] == method and path['description'] == description and path.get(
                'deprecated', False) for path in paths_info)

        if is_deprecated:
            continue  # Пропускаем устаревшие эндпоинты

        types = set(call_type[(method, endpoint, description)])
        total_endpoints += 1
        total_calls_excluding_generation += count

        coverage_status = "Недостаточное покрытие ❌"
        present_types = [test_type for test_type in required_types if test_type in types]
        coverage_count = len(present_types)
        required_count = len(required_types)

        # Добавленная логика для проверки на exception_types
        if any(exception_type in types for exception_type in exception_types):
            coverage_percentage = 100
            coverage_status = "Покрытие выполнено на 100% ✅ (исключение)"
        elif coverage_count == required_count:
            coverage_percentage = 100
            coverage_status = "Покрытие выполнено ✅"
        elif coverage_count > 0:
            coverage_percentage = (coverage_count / required_count) * 100
            coverage_status = f"Покрытие выполнено на {coverage_percentage:.2f}% 🔔"
        else:
            coverage_percentage = 0

        total_coverage_percentage += coverage_percentage

        # Сохраняем отчет для конкретного Swagger API
        swagger_title = "Swagger API"  # Здесь вы можете получить название из swagger_settings
        if swagger_title not in swagger_reports:
            swagger_reports[swagger_title] = []

        report_line = (
            f"\n{description}\nЭндпоинт: {endpoint}\nМетод: {method} | "
            f"Обращений: {count}, Типы тестов: {', '.join(types)}\n{coverage_status}\n"
        )
        swagger_reports[swagger_title].append(report_line)

    # Расчет общего процента покрытия
    if total_endpoints > 0:
        average_coverage_percentage = total_coverage_percentage / total_endpoints
    else:
        average_coverage_percentage = 0

    # Вкладка с общей оценкой покрытия
    border = "*" * 50
    summary = f"{border}\nОбщий процент покрытия: {average_coverage_percentage:.2f}%\nОбщее количество вызовов: {total_calls_excluding_generation}\n{border}\n"
    report_lines.insert(0, summary)


    # Добавляем общую оценку покрытия
    allure.attach("\n".join(report_lines), name='Общая оценка покрытия', attachment_type=allure.attachment_type.TEXT)

    # Создаем график
    create_chart(call_count)
    with open('api_call_counts.png', 'rb') as f:
        allure.attach(f.read(), name='Оценка покрытия', attachment_type=allure.attachment_type.PNG)

    # Добавляем отчеты для каждого Swagger API
    for swagger_title, lines in swagger_reports.items():
        allure.attach("\n".join(lines), name=swagger_title, attachment_type=allure.attachment_type.TEXT)
