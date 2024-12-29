import logging
from datetime import datetime
import os
import pytest
import sys

from gitanalyzer import Repository, Git
from gitanalyzer.repository import MalformedUrl

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


@pytest.fixture
def repository(request):
    return list(Repository(path_to_repo=request.param).traverse_commits())


@pytest.fixture
def repository_to(request):
    path, to = request.param
    return list(Repository(path_to_repo=path, to=to).traverse_commits())


@pytest.fixture()
def git_repository(request):
    git_repo = Git(request.param)
    yield git_repo
    git_repo.clear()


# It should raise an error when no URLs are provided
def test_no_url_provided():
    with pytest.raises(Exception):
        list(Repository().traverse_commits())


# It should raise an error when the URL format is incorrect
def test_incorrect_url_format():
    with pytest.raises(Exception):
        list(Repository(path_to_repo=set('repo')).traverse_commits())


# It should raise an error when the URL is malformed
def test_url_malformation():
    with pytest.raises(MalformedUrl):
        list(Repository("https://badurl.git/").traverse_commits())


@pytest.mark.parametrize('repository,expected', [
    ("test-repos/small_repo", 5)
], indirect=['repository'])
def test_single_local_url(repository, expected):
    assert len(repository) == expected


@pytest.mark.parametrize('repository,expected', [
    ((["test-repos/small_repo", "test-repos/branches_merged"]), 9)
], indirect=['repository'])
def test_multiple_local_urls(repository, expected):
    assert len(repository) == expected


@pytest.mark.parametrize('repository_to,expected', [
    (("https://github.com/codingwithshawnyt/GitAnalyzer.git", datetime(2018, 10, 20)), 159)
], indirect=['repository_to'])
def test_single_remote_url(repository_to, expected):
    assert len(repository_to) == expected


@pytest.mark.parametrize('repository_to,expected', [
    ((["https://github.com/codingwithshawnyt/GitAnalyzer.git",
      "https://github.com/codingwithshawnyt/GitAnalyzer"], datetime(2018, 10, 20)),
     518)
], indirect=['repository_to'])
def test_multiple_remote_urls(repository_to, expected):
    assert len(repository_to) == expected


@pytest.mark.parametrize('repository,expected', [
    ((["test-repos/small_repo", "test-repos/small_repo"]), 10)
], indirect=['repository'])
def test_duplicate_local_urls(repository, expected):
    assert len(repository) == expected


@pytest.mark.parametrize('repository_to,expected', [
    ((["test-repos/small_repo", "https://github.com/codingwithshawnyt/GitAnalyzer.git"],
     datetime(2018, 10, 20)),
     164)
], indirect=['repository_to'])
def test_local_and_remote_urls(repository_to, expected):
    assert len(repository_to) == expected


@pytest.mark.parametrize('repository_to,expected', [
    ((["test-repos/small_repo", "https://github.com/codingwithshawnyt/GitAnalyzer.git",
      "test-repos/branches_merged", "https://github.com/codingwithshawnyt/GitAnalyzer.git"],
     datetime(2018, 10, 20)),
     527)
], indirect=['repository_to'])
def test_combined_local_and_remote_urls(repository_to, expected):
    assert len(repository_to) == expected


def test_url_format_issues():
    with pytest.raises(Exception):
        list(Repository(
            path_to_repo='https://github.com/codingwithshawnyt/GitAnalyzer.git/test')
             .traverse_commits())

    with pytest.raises(Exception):
        list(Repository(path_to_repo='test').traverse_commits())


@pytest.mark.parametrize('git_repository', ["test-repos/histogram"], indirect=True)
def test_diff_without_histogram(git_repository):
    # without histogram
    commit = list(Repository('test-repos/histogram',
                             single="93df8676e6fab70d9677e94fd0f6b17db095e890").traverse_commits())[0]

    diff = commit.modified_files[0].diff_parsed
    assert len(diff['added']) == 11
    assert (3, '    if (path == null)') in diff['added']
    assert (5, '        log.error("Icon path is null");') in diff['added']
    assert (6, '        return null;') in diff['added']
    assert (8, '') in diff['added']
    assert (9, '    java.net.URL imgURL = GuiImporter.class.getResource(path);') in diff['added']
    assert (10, '') in diff['added']
    assert (11, '    if (imgURL == null)') in diff['added']
    assert (12, '    {') in diff['added']
    assert (14, '        return null;') in diff['added']
    assert (16, '    else') in diff['added']
    assert (17, '        return new ImageIcon(imgURL);') in diff['added']

    assert len(diff['deleted']) == 7
    assert (3, '    java.net.URL imgURL = GuiImporter.class.getResource(path);') in diff['deleted']
    assert (4, '') in diff['deleted']
    assert (5, '    if (imgURL != null)') in diff['deleted']
    assert (7, '        return new ImageIcon(imgURL);') in diff['deleted']
    assert (9, '    else') in diff['deleted']
    assert (10, '    {') in diff['deleted']
    assert (13, '    return null;') in diff['deleted']


@pytest.mark.parametrize('git_repository', ["test-repos/histogram"], indirect=True)
def test_diff_with_histogram(git_repository):
    # with histogram
    commit = list(Repository('test-repos/histogram',
                             single="93df8676e6fab70d9677e94fd0f6b17db095e890",
                             histogram_diff=True).traverse_commits())[0]
    diff = commit.modified_files[0].diff_parsed
    assert (4, '    {') in diff["added"]
    assert (5, '        log.error("Icon path is null");') in diff["added"]
    assert (6, '        return null;') in diff["added"]
    assert (7, '    }') in diff["added"]
    assert (8, '') in diff["added"]
    assert (11, '    if (imgURL == null)') in diff["added"]
    assert (12, '    {') in diff["added"]
    assert (13, '        log.error("Couldn\'t find icon: " + imgURL);') in diff["added"]
    assert (14, '        return null;') in diff["added"]
    assert (17, '        return new ImageIcon(imgURL);') in diff["added"]

    assert (6, '    {') in diff["deleted"]
    assert (7, '        return new ImageIcon(imgURL);') in diff["deleted"]
    assert (10, '    {') in diff["deleted"]
    assert (11, '        log.error("Couldn\'t find icon: " + imgURL);') in diff["deleted"]
    assert (12, '    }') in diff["deleted"]
    assert (13, '    return null;') in diff["deleted"]


def test_ignore_whitespace_additions():
    commit = list(Repository('test-repos/whitespace',
                             single="338a74ceae164784e216555d930210371279ba8e").traverse_commits())[0]
    assert len(commit.modified_files) == 1
    commit = list(Repository('test-repos/whitespace',
                             skip_whitespaces=True,
                             single="338a74ceae164784e216555d930210371279ba8e").traverse_commits())[0]
    assert len(commit.modified_files) == 0


@pytest.mark.parametrize('git_repository', ["test-repos/whitespace"], indirect=True)
def test_ignore_whitespace_changes_and_normal_line_modifications(git_repository):
    commit = list(Repository('test-repos/whitespace',
                             single="52716ef1f11e07308b5df1b313aec5496d5e91ce").traverse_commits())[0]
    assert len(commit.modified_files) == 1
    parsed_normal_diff = commit.modified_files[0].diff_parsed
    commit = list(Repository('test-repos/whitespace',
                             skip_whitespaces=True,
                             single="52716ef1f11e07308b5df1b313aec5496d5e91ce").traverse_commits())[0]
    assert len(commit.modified_files) == 1
    parsed_wo_whitespaces_diff = commit.modified_files[0].diff_parsed
    assert len(parsed_normal_diff['added']) == 2
    assert len(parsed_wo_whitespaces_diff['added']) == 1

    assert len(parsed_normal_diff['deleted']) == 1
    assert len(parsed_wo_whitespaces_diff['deleted']) == 0


def test_ignore_whitespace_deletions():
    commit = list(Repository('test-repos/whitespace',
                             single="e6e429f6b485e18fb856019d9953370fd5420b20").traverse_commits())[0]
    assert len(commit.modified_files) == 1
    commit = list(Repository('test-repos/whitespace',
                             skip_whitespaces=True,
                             single="e6e429f6b485e18fb856019d9953370fd5420b20").traverse_commits())[0]
    assert len(commit.modified_files) == 0


def test_ignore_whitespace_additions_and_file_changes():
    commit = list(Repository('test-repos/whitespace',
                             single="532068e9d64b8a86e07eea93de3a57bf9e5b4ae0").traverse_commits())[0]
    assert len(commit.modified_files) == 2
    commit = list(Repository('test-repos/whitespace',
                             skip_whitespaces=True,
                             single="532068e9d64b8a86e07eea93de3a57bf9e5b4ae0").traverse_commits())[0]
    assert len(commit.modified_files) == 1


def test_clone_repository_to(tmp_path):
    dt2 = datetime(2018, 10, 20)
    url = "https://github.com/codingwithshawnyt/GitAnalyzer.git"
    assert len(list(Repository(
        path_to_repo=url,
        to=dt2,
        clone_repo_to=str(tmp_path)).traverse_commits())) == 159
    assert tmp_path.exists() is True


def test_clone_repository_to_nonexistent_directory():
    with pytest.raises(Exception):
        list(Repository("https://github.com/codingwithshawnyt/GitAnalyzer",
                        clone_repo_to="NONEXISTENTDIR").traverse_commits())


def test_clone_repository_to_existing_directory():
    import tempfile
    tmp_path = tempfile.gettempdir()
    dt2 = datetime(2018, 10, 20)
    url = "https://github.com/codingwithshawnyt/GitAnalyzer.git"
    assert len(list(Repository(
        path_to_repo=url,
        to=dt2,
        clone_repo_to=str(tmp_path)).traverse_commits())) == 159
    assert os.path.isdir(os.path.join(tmp_path, "GitAnalyzer"))
    assert len(list(Repository(
        path_to_repo=url,
        to=dt2,
        clone_repo_to=str(tmp_path)).traverse_commits())) == 159
    assert os.path.isdir(os.path.join(tmp_path, "GitAnalyzer"))


def test_project_name_with_multiple_repositories():
    repositories = [
        'test-repos/files_in_directories',
        'test-repos/files_in_directories',
        'test-repos/files_in_directories'
    ]
    for commit in Repository(path_to_repo=repositories).traverse_commits():
        assert commit.project_name == 'files_in_directories'


def test_project_name_with_remote_and_local_repositories():
    repositories = [
        'https://github.com/codingwithshawnyt/GitAnalyzer',
        'test-repos/GitAnalyzer'
    ]
    for commit in Repository(path_to_repo=repositories).traverse_commits():
        assert commit.project_name == 'GitAnalyzer'


def test_extract_repository_name_from_url():
    # with .git in the middle of the name
    url_set_a = [
        "https://github.com/academicpages/academicpages.github.io",
        "https://github.com/academicpages/academicpages.github.io.git",
    ]

    url_set_b = [
        "https://github.com/codingwithshawnyt/GitAnalyzer",
        "https://github.com/codingwithshawnyt/GitAnalyzer.git",
    ]

    for url in url_set_a:
        assert Repository._get_repo_name_from_url(url) == "academicpages.github.io"

    for url in url_set_b:
        assert Repository._get_repo_name_from_url(url) == "GitAnalyzer"


@pytest.mark.skipif(sys.version_info < (3, 8) and sys.platform == "win32", reason="requires Python3.8 or greater on Windows")
def test_cleanup_remote_repositories():
    repositories = [
        'https://github.com/codingwithshawnyt/GitAnalyzer',
        'https://github.com/codingwithshawnyt/GitAnalyzer'
    ]
    paths = set()
    for commit in Repository(path_to_repo=repositories).traverse_commits():
        paths.add(commit.project_path)

    for path in paths:
        assert os.path.exists(path) is False


def test_deleted_files_in_repository():
    deleted_commits = list(
        Repository('https://github.com/codingwithshawnyt/GitAnalyzer',
                   filepath='.bettercodehub.yml',
                   include_deleted_files=True).traverse_commits()
    )
    assert len(deleted_commits) > 0