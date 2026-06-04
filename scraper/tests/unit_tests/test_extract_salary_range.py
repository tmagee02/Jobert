import pytest
from scraper.handleNLP import extractSalaryRange


@pytest.mark.parametrize(
    'text, expected',
    [
        ('$147,400 and $272,100 SALARY', (147400, 272100)),
        ('$190,400 - $285,600', (190400, 285600)),
        ('$64,000—$204,000', (64000, 204000)),
        ('USD$171,000 per year - USD$190,000', (171000, 190000)),
        ('$29K – $325K', (29000, 325000)),
        ('$2k – $32k', (2000, 32000)),
        ('$171,000', (171000, 171000)),
        ('$2K', (2000, 2000)),
        ('$190,800.00 - $262,800.00 per year', (190800, 262800)), #Plaid
        ('$2,000.00 per year', (2000, 2000)), #Plaid
        ('$240,000 - $300,000', (240000, 300000)), #Brax
        ('$203,410–290,586 USD', (203410, 290586)), #Spotify
        ('US: $174000 - $253000 (USD)', (174000, 253000)), #Google
    ]
)
def test_extract_salary_range(text, expected):
    assert extractSalaryRange(text) == expected


@pytest.mark.parametrize(
    'text', 
    [
        '',
        'Salary: ',
        '$147,400 and $272,100 and $347,400',
        # pytest.param('', marks=pytest.mark.skip(reason='need to grab other examples')),
        # pytest.param('', marks=pytest.mark.skip(reason='need to grab other examples')),
        # pytest.param('', marks=pytest.mark.skip(reason='need to grab other examples')),
        # pytest.param('', marks=pytest.mark.skip(reason='need to grab other examples')),
        # pytest.param('', marks=pytest.mark.skip(reason='need to grab other examples')),
    ]
)
def test_extract_salary_range_invalid_format(text):
    with pytest.raises(ValueError):
        extractSalaryRange(text)


@pytest.mark.parametrize(
    'bad_type',
    [
        None,
        1,
        2.3,
        True,
        []
    ]
)
def test_extract_salary_invalid_type(bad_type):
    with pytest.raises(TypeError):
        extractSalaryRange(bad_type)