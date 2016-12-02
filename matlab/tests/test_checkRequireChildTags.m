function test_suite = test_checkRequireChildTags%#ok<STOUT>
initTestSuite;

function values = setup %#ok<DEFNU>
% Read in the HED schema
values.Tags1 = {};
values.Tags2 = {'Event/Category', 'Event/Duration'};
values.Tags3 = {'Event/Label/Test', {'Event/Category', ...
    'Event/Duration'}};
load('HEDMaps.mat');
values.hedMaps = hedMaps;

function teardown(values) %#ok<INUSD,DEFNU>
% Function executed after each test


function testRequireChildTags(values)  %#ok<DEFNU>
% Unit test for editmaps
fprintf('\nUnit tests for checkrequirechild\n');

fprintf('\nIt should return no errors when there are no tags present');
[errors, tags] = checkRequireChildTags(values.hedMaps, values.Tags1, ...
    values.Tags1);
assertTrue(isempty(errors));
assertTrue(isempty(tags));

fprintf(['\nIt should return errors when there are tags that require' ...
    ' children present\n']);
[errors, tags] = checkRequireChildTags(values.hedMaps, values.Tags2, ...
    values.Tags2);
assertFalse(isempty(errors));
assertFalse(isempty(tags));
assertEqual(length(tags), 2);

fprintf(['\nIt should return errors when there are tags in a tag group' ...
    ' that require children present\n']);
[errors, tags] = checkRequireChildTags(values.hedMaps, values.Tags3, ...
    values.Tags3);
assertFalse(isempty(errors));
assertFalse(isempty(tags));
assertEqual(length(tags), 2);