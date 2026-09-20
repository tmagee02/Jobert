import pytest
from scraper.processNLP import extractExperience


@pytest.mark.parametrize(
    'experienceEntities, expected', 
    [
        (['10 years EXPERIENCE'], (10, None)),
        (['3+ years EXPERIENCE'], (3, None)),
        (['5-8 years EXPERIENCE'], (5, 8)),
        ([], (None, None))
    ]
)
def test_extract_experience_valid(experienceEntities, expected):
    url = 'www.unittest.com'
    assert extractExperience(url, experienceEntities) == expected


@pytest.mark.parametrize(
    'experienceEntities',
    [
        ['Experience Needed'],
        [''],
        ['10-20-30 years EXPERIENCE']
    ]
)
def test_extract_experience_invalid_value_count(experienceEntities, caplog):
    url = 'www.unittest.com'
    assert extractExperience(url, experienceEntities) == (None, None)
    assert f'{url} - Unexpected amount of values in experience string - {experienceEntities[0]}' in caplog.text


@pytest.mark.parametrize(
    'experienceEntities',
    [
        ['9-7 years EXPERIENCE'],
        ['10-100 years EXPERIENCE'],
        pytest.param('-1-8 years EXPERIENCE', marks=pytest.mark.xfail(reason='negative values not currently handled properly'))
    ]
)
def test_extract_experience_invalid_yoe(experienceEntities, caplog):
    url = 'www.unittest.com'
    assert extractExperience(url, experienceEntities) == (None, None)
    assert f'{url} - Unexpected years of experience in experience string - {experienceEntities[0]}' in caplog.text


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
def test_extract_experience_invalid_type(bad_type):
    with pytest.raises(TypeError):
        extractExperience(bad_type)