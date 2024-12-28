import muuusiiik.util as msk
import os

from   pytest import raises


# -----------------------------
# MOCK :: CREATE & REMOVE FILE
# -----------------------------
class Mock:
    def make_sure_there_is_a_file(file_name:str):
        fd, fn = msk.data.path_split(file_name)
        msk.data.make_path(fd)
        msk.data.save('', file_name)

    def make_sure_the_folder_removed(path:str):
        msk.data.rm(path)

    def make_a_new_folder_with_3_files_1_folder_inside(folder, fname):
        # mock a new folder with 3 files and 1 folder inside
        Mock.make_sure_the_folder_removed(folder)
        file_name = f'{folder}/{fname}'
        for i in range(3): Mock.make_sure_there_is_a_file(f'{file_name}_{i:02}.txt')
        msk.data.make_path(f'{folder}/not_exist_folder', pathtype='folder')

    def make_content_files(folder_path, contents):
        for k, v in contents.items():
            f = f'{folder_path}/{k}'
            msk.data.save(v, f)


# -----------------------------
# FILE PATH SPLIT 
# -----------------------------
def test_path_split_on_folder_path():
    file_name = '/some/folder_path/'
    fd, fn    = msk.data.path_split(file_name)
    assert (fd, fn) == ('/some/folder_path', '')
    

def test_path_split_on_file_path():
    file_name = '/some/folder_path/file_name.txt'
    fd, fn    = msk.data.path_split(file_name)
    assert (fd, fn) == ('/some/folder_path', 'file_name.txt')
    

def test_path_split_on_current_folder():
    # current path with filename
    file_name = 'file_name.txt'
    fd, fn    = msk.data.path_split(file_name)
    assert (fd, fn) == ('.', 'file_name.txt')

    # nothing in the path
    file_name = ''
    fd, fn    = msk.data.path_split(file_name)
    assert (fd, fn) == ('.', '')

    # current path is .
    file_name = '.'
    fd, fn    = msk.data.path_split(file_name)
    assert (fd, fn) == ('.', '')

    # file_name is single letter
    file_name = 'x'
    fd, fn    = msk.data.path_split(file_name)
    assert (fd, fn) == ('.', 'x')


def test_path_split_raise_attribute_error():
    with raises(AttributeError):
        filename = 1
        p, f     = msk.data.path_split(filename)


# -----------------------------
# CHECK TYPE OF FILE & FOLDER 
# -----------------------------
def test_path_type_is_file_when_give_file_path():
    path   = 'tests/test_data.py'
    result = msk.data.path_type(path)
    assert result == 'file'


def test_path_type_is_folder_when_give_folder_path():
    # with out slash
    path   = 'tests'
    result = msk.data.path_type(path)
    assert result == 'folder'

    # with slash
    path   = 'tests/'
    result = msk.data.path_type(path)
    assert result == 'folder'


def test_path_type_is_current_dir_represented_with_special_char():
    # path is dot
    path   = '.'
    result = msk.data.path_type(path)
    assert result == 'folder'

    # path is empty string
    path   = ''
    result = msk.data.path_type(path)
    assert result == 'folder'


def test_path_type_is_none_when_give_non_existing_path():
    path   = 'tests/non_existing_file.txt'
    result = msk.data.path_type(path)
    assert result == None


# -----------------------------
# CHECK IF FILE & FOLDER EXIST
# -----------------------------
def test_there_is_existing_file():
    file_name = 'tests/test_data.py'
    result    = msk.data.exist(file_name)
    assert result == True


def test_there_is_existing_file_without_folder_path():
    file_name = 'README.md'
    result    = msk.data.exist(file_name)
    assert result == True


def test_there_is_not_existing_file():
    file_name = 'tests/non_existing_file.py'
    result    = msk.data.exist(file_name)
    assert result == False


def test_there_is_existing_folder():
    # without slash
    folder_name = 'tests'
    result      = msk.data.exist(folder_name)
    assert result == True

    # with slash
    folder_name = 'tests/'
    result      = msk.data.exist(folder_name)
    assert result == True


def test_exist_current_folder_with_special_char():
    # current folder is dot
    folder_name = '.'
    result      = msk.data.exist(folder_name)
    assert result == True

    # current folder is empty string
    folder_name = ''
    result      = msk.data.exist(folder_name)
    assert result == True


def test_there_is_no_exising_folder():
    folder_name = 'not_existing_tests/'
    result      = msk.data.exist(folder_name)
    assert result == False


def test_raise_type_error_for_incorrect_path_type():
    with raises(TypeError):
        folder_name = 'not_existing_tests/'
        result      = msk.data.exist(folder_name, pathtype='document')


# -----------------------------
# LS A SPECIFIC PATH
# -----------------------------
def test_list_contents_in_a_given_folder_in_list_format():
    # mock a new folder with 3 files and 1 folder inside
    file_name = 'tests/_data/some_file'
    fd, fn    = msk.data.path_split(file_name)
    Mock.make_a_new_folder_with_3_files_1_folder_inside(fd, fn)

    # check ontents in given folder
    result    = msk.data.ls(fd)
    assert len(result) == 4
    assert ('not_exist_folder/' in result) == True
    assert ('some_file_00.txt'  in result) == True
    assert ('some_file_01.txt'  in result) == True
    assert ('some_file_02.txt'  in result) == True
    assert ('some_file_03.txt'  in result) == False

    # remove the folder
    Mock.make_sure_the_folder_removed(fd)
    assert msk.data.exist(fd) == False


def test_list_contents_in_a_given_folder_in_dict_format():
    # mock a new folder with 3 files and 1 folder inside
    file_name = 'tests/_data/some_file'
    fd, fn    = msk.data.path_split(file_name)
    Mock.make_a_new_folder_with_3_files_1_folder_inside(fd, fn)

    # check ontents in given folder
    result    = msk.data.ls(fd, fmt='dict')
    assert len(result) == 2
    assert len(result['folder']) == 1
    assert len(result['file'  ]) == 3
    assert ('not_exist_folder' in result['folder']) == True
    assert ('some_file_00.txt' in result['file'  ]) == True
    assert ('some_file_01.txt' in result['file'  ]) == True
    assert ('some_file_02.txt' in result['file'  ]) == True
    assert ('some_file_03.txt' in result['file'  ]) == False

    # remove the folder
    Mock.make_sure_the_folder_removed(fd)
    assert msk.data.exist(fd) == False


def test_list_contents_in_current_folder_with_special_char():
    path   = '.'
    result = msk.data.ls(path)
    assert ('README.md' in result)         == True
    assert ('not_existing_file' in result) == False

    path   = ''
    result = msk.data.ls(path)
    assert ('README.md' in result)         == True
    assert ('not_existing_file' in result) == False


def test_list_contents_in_a_non_existing_folder():
    path   = 'non_existing_path'
    with raises(FileNotFoundError):
        result = msk.data.ls(path)


def test_list_conents_in_a_path_the_same_as_file_name():
    path   = 'tests/test_data.py'
    with raises(NotADirectoryError):
        result = msk.data.ls(path)


# -----------------------------
# REMOVE FILE & FOLDER
# -----------------------------
def test_remove_a_file():
    # mock content 
    file_name = 'tests/_data/some_file'
    fd, fn    = msk.data.path_split(file_name)
    Mock.make_a_new_folder_with_3_files_1_folder_inside(fd, fn)

    # the mocked contents have 3 files and 1 folder
    ls_list   = msk.data.ls(fd)
    assert len(ls_list) == 4

    # remove file 01
    f         = f'{file_name}_01.txt'
    result    = msk.data.rm(f)
    ls_list   = msk.data.ls(fd)
    assert result         == True
    assert len(ls_list)   == 3
    assert (f in ls_list) == False

    # reset to zero
    Mock.make_sure_the_folder_removed(fd)
    assert msk.data.exist(fd) == False


def test_remove_a_folder():
    # mock content 
    file_name = 'tests/_data/some_file'
    fd, fn    = msk.data.path_split(file_name)
    Mock.make_a_new_folder_with_3_files_1_folder_inside(fd, fn)

    # remove tests/_data/
    result    = msk.data.rm(fd)
    assert result == True

    # folder tests/_data/ does not exist anymore in tests/
    ls_list   = msk.data.ls('tests')
    assert (fd in ls_list) == False


def test_remove_a_non_existing_file():
    file_name = 'tests/non_existing_file.txt'
    result    = msk.data.rm(file_name)
    assert result == False


def test_remove_a_non_existing_folder():
    folder_path = 'tests/non_existing_folder/'
    result      = msk.data.rm(folder_path)
    assert result == False


# -----------------------------
# MAKE PATH
# -----------------------------
def test_make_path_from_various_paths():
    # make sure tests/_data/ folder is not exist
    result = msk.data.rm('tests/_data')

    # #make a folder for testing this demo
    path   = 'tests/_data'
    result = msk.data.make_path(path, pathtype='folder')
    assert result == True

    # make a folder from file_path
    path   = 'tests/_data/non_existing_folder_01/with_file.txt'
    result = msk.data.make_path(path)
    assert result == True

    # make a folder from folder_path with ending slash, pathtype=file
    path   = 'tests/_data/non_existing_folder_02/'
    result = msk.data.make_path(path, pathtype='file')
    assert result == True

    # make a folder from folder_path with ending slash, pathtype=folder
    path   = 'tests/_data/non_existing_folder_03/'
    result = msk.data.make_path(path, pathtype='folder')
    assert result == True

    # make a folder from folder_path WITHOUT ending slash, pathtype=file >> do not make a folder
    path   = 'tests/_data/non_existing_folder_04'
    result = msk.data.make_path(path, pathtype='file')
    assert result == True

    # make a folder from folder_path WITHOUT ending slash, pathtype=folder >> a folder created
    path   = 'tests/_data/non_existing_folder_05'
    result = msk.data.make_path(path, pathtype='folder')
    assert result == True

    # ASSERTATION CHECK
    result = msk.data.ls('tests/_data', fmt='dict')
    assert len(result['folder']) == 4
    assert len(result['file'  ]) == 0
    assert ('non_existing_folder_04' in result['folder']) == False

    # reset content
    result = msk.data.rm('tests/_data')
    assert result == True
    result = msk.data.ls('tests/')
    assert ('_data' in result) == False


# -----------------------------
# SAVE AND LOAD CONTENT
# -----------------------------
def test_save_non_content_and_get_type_error():
    """ if content is None then create and empty file"""
    # resest the folder
    Mock.make_sure_the_folder_removed('tests/_data')
    # create a file
    path    = 'tests/_data/saved_content.txt'
    content = None
    msk.data.save(content, path)
    # check the file exist
    result  = msk.data.exist(path)
    assert result == True
    # content is empty string
    content = msk.data.load(path)
    assert content == ['']
    # resest the folder
    Mock.make_sure_the_folder_removed('tests/_data')


def test_load_incorrect_path():
    path   = 'tests/_data/content.txt'
    fd, fn = msk.data.path_split(path)
    Mock.make_sure_the_folder_removed(fd)

    with raises(FileNotFoundError):
        content = msk.data.load(path)


def test_save_and_load_object():
    # resest the folder
    content_folder = 'tests/_data'
    Mock.make_sure_the_folder_removed(content_folder)
    # create a dict content
    path    = f'{content_folder}/dict.bin'
    content = {'type': 'object'}
    msk.data.save_object(content, path)
    # check the file exist
    result  = msk.data.exist(path)
    assert result == True
    # content is empty string
    loaded_dict = msk.data.load_object(path)
    assert loaded_dict == {'type': 'object'}

    # create a list content
    path    = f'{content_folder}/list.bin'
    content = [1,2,3,4]
    msk.data.save_object(content, path)
    # check the file exist
    result  = msk.data.exist(path)
    assert result == True
    # content is empty string
    loaded_list = msk.data.load_object(path)
    assert loaded_list == [1,2,3,4]

    # other asserts
    ls_list = msk.data.ls(content_folder)
    assert len(ls_list) == 2
    assert ('dict.bin' in ls_list) == True
    assert ('list.bin' in ls_list) == True

    # resest the folder
    Mock.make_sure_the_folder_removed(content_folder)
    result  = msk.data.exist(content_folder)
    assert result == False


def test_save_and_load_plain_text():
    # resest the folder
    content_folder = 'tests/_data'
    Mock.make_sure_the_folder_removed(content_folder)

    # create a plain_text content
    path    = f'{content_folder}/one_line.txt'
    content = 'hello'
    msk.data.save(content, path)
    # check the file exist
    result  = msk.data.exist(path)
    assert result == True
    # content is 'hello'
    loaded_content = msk.data.load(path)
    assert loaded_content == ['hello']

    # create a list of string content
    path    = f'{content_folder}/multiple_lines.txt'
    content = ['hello', 'world']
    msk.data.save(content, path)
    # check the file exist
    result  = msk.data.exist(path)
    assert result == True
    # content is ['hello' 'world']
    loaded_content = msk.data.load(path)
    assert loaded_content == ['hello', 'world']

    # other asserts
    ls_list = msk.data.ls(content_folder)
    assert len(ls_list) == 2
    assert ('one_line.txt'       in ls_list) == True
    assert ('multiple_lines.txt' in ls_list) == True

    # resest the folder
    Mock.make_sure_the_folder_removed(content_folder)
    result  = msk.data.exist(content_folder)
    assert result == False


# -----------------------------
# LOAD CONTENT FROM FILE LIST
# -----------------------------
def test_load_list_of_files():
    # create list of files - 2 files
    folder_path = 'tests/_data'
    contents    = { 'f1.txt': ['a01', 'a02', ' ', 'a03', 'a4'],
                    'f2.txt': ['b01', 'b02', 'a03'] }
    Mock.make_content_files(folder_path, contents)

    # check if the files created properly
    f_list = [f'{folder_path}/{f}' for f in contents.keys()]

    # load conents from the list
    load_condition = lambda v: v.startswith('a')
    result1 = msk.data.load_file_list(f_list)           # ignore content that is whitespace
    result2 = msk.data.load_file_list(f_list, n_char=2) # ignore content that less than n_char
    result3 = msk.data.load_file_list(f_list, n_char=2, load_condition=load_condition) # overwrite n_char with load_condition

    # assertations
    for f in f_list: assert msk.data.exist(f) == True
    # - case result1
    assert len(result1) == 7
    assert ('a01' in result1) == True
    assert ('b02' in result1) == True
    assert ('b03' in result1) == False
    # - case result2
    assert len(result2) == 6
    assert ('a01' in result2) == True
    assert ('b02' in result2) == True
    assert ('a4'  in result2) == False
    # - case result3
    assert len(result3) == 5
    assert ('a01' in result3) == True
    assert ('b02' in result3) == False
    assert ('a4'  in result3) == True

    # reset the folder
    Mock.make_sure_the_folder_removed(folder_path)
    result = msk.data.exist(folder_path)
    assert result == False


# -----------------------------
# LOAD CATEGORY MAPPER CONTENT 
# -----------------------------
def test_category_mapper():
    # create list of files - 2 files
    folder_path     = 'tests/_data'
    contents = {'animal.txt': ['mammal,dog,cat', 'reptile,snake, croc, komodo'],
                'number.txt': ['digit,1,2,3','eng,one, two , three, twenty four '],
                'food.txt':   ['herb,', 'noodle, ramen, somen'] }
    Mock.make_content_files(folder_path, contents)

    # check if the files created properly
    f_list = [f'{folder_path}/{f}' for f in contents.keys()]

    # load contents from teh list
    cate, mapper  = msk.data.category_mapper(f_list)
    ls_list = msk.data.ls(folder_path)

    # assertations
    for f in f_list: assert msk.data.exist(f) == True
    assert len(ls_list) == 3
    assert set(ls_list) == set(list(contents.keys()))

    assert len(cate)       == 6
    assert cate['mammal' ] == ['mammal', 'dog', 'cat']
    assert cate['reptile'] == ['reptile', 'snake', 'croc', 'komodo']
    assert cate['herb'   ] == ['herb']
    assert ('two'         in cate['eng']) == True
    assert ('twenty four' in cate['eng']) == True

    assert len(mapper)    == 20
    assert mapper['two']  == 'eng'
    assert mapper['herb'] == 'herb'

    # reset the folder
    Mock.make_sure_the_folder_removed(folder_path)
    result = msk.data.exist(folder_path)
    assert result == False
