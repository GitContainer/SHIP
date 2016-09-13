import unittest

from ship.isis.datcollection import DatCollection
from ship.isis.isisunitfactory import IsisUnitFactory as iuf
from ship.isis.datunits import riverunit, ROW_DATA_TYPES
from ship.utils.filetools import PathHolder


class IsisUnitCollectionTest(unittest.TestCase):
    '''Test for the IsisUnitCollection class.
    '''
     
    def setUp(self):
        '''Set up stuff that will be used throughout the class.
        '''
        self.fake_path = 'c:\\fake\\path\\to\\file.dat'
        self.path_holder = PathHolder(self.fake_path)
        # Create a couple of unit to use in the methods.
        self.unit_contents1 = \
        ['RIVER (Culvert Exit) CH:7932 - Trimmed to BT\n',
         'SECTION\n',
         '1.067\n',
         '    15.078            1.111111      1000\n',
         '        18\n',
         '     5.996    37.560     0.080     1.000LEFT       291391.67  86582.61LEFT      16        \n',
         '     6.936    37.197     0.035*    1.000           291391.43  86581.70          \n',
         '     7.446    36.726     0.035     1.000           291391.30  86581.21          \n',
         '     7.635    35.235     0.035     1.000           291391.25  86581.03          \n',
         '     8.561    35.196     0.035     1.000           291391.01  86580.13          \n',
         '     9.551    35.190     0.035     1.000BED        291390.75  86579.18          \n',
         '    10.323    35.229     0.035     1.000           291390.55  86578.43          \n',
         '    10.904    35.319     0.035     1.000           291390.40  86577.87          \n',
         '    12.542    35.637     0.035     1.000           291389.98  86576.29          \n',
         '    13.740    35.593     0.035     1.000           291389.67  86575.13          \n',
         '    13.788    35.592     0.035     1.000           291389.66  86575.09          \n',
         '    13.944    36.148     0.035     1.000           291389.62  86574.93          \n',
         '    15.008    36.559     0.080*    1.000           291389.34  86573.91          \n',
         '    16.355    37.542     0.080     1.000           291389.00  86572.60          \n',
         '    17.424    38.518     0.080     1.000           291388.72  86571.57          \n',
         '    18.449    39.037     0.080     1.000           291388.46  86570.58          \n',
         '    19.416    39.146     0.080     1.000           291388.21  86569.65          \n',
         '    19.420    39.133     0.080     1.000RIGHT      291388.21  86569.65RIGHT     4095      \n']

        self.unit_contents2 = \
        ['RIVER (Culvert Exit) CH:7932 - Trimmed to BT\n',
         'SECTION\n',
         '1.068\n',
         '    15.078            1.111111      1000\n',
         '        18\n',
         '     5.996    37.560     0.080     1.000LEFT       291391.67  86582.61LEFT      16        \n',
         '     6.936    37.197     0.035*    1.000           291391.43  86581.70          \n',
         '     7.446    36.726     0.035     1.000           291391.30  86581.21          \n',
         '     7.635    35.235     0.035     1.000           291391.25  86581.03          \n',
         '     8.561    35.196     0.035     1.000           291391.01  86580.13          \n',
         '     9.551    35.190     0.035     1.000BED        291390.75  86579.18          \n',
         '    10.323    35.229     0.035     1.000           291390.55  86578.43          \n',
         '    10.904    35.319     0.035     1.000           291390.40  86577.87          \n',
         '    12.542    35.637     0.035     1.000           291389.98  86576.29          \n',
         '    13.740    35.593     0.035     1.000           291389.67  86575.13          \n',
         '    13.788    35.592     0.035     1.000           291389.66  86575.09          \n',
         '    13.944    36.148     0.035     1.000           291389.62  86574.93          \n',
         '    15.008    36.559     0.080*    1.000           291389.34  86573.91          \n',
         '    16.355    37.542     0.080     1.000           291389.00  86572.60          \n',
         '    17.424    38.518     0.080     1.000           291388.72  86571.57          \n',
         '    18.449    39.037     0.080     1.000           291388.46  86570.58          \n',
         '    19.416    39.146     0.080     1.000           291388.21  86569.65          \n',
         '    19.420    39.133     0.080     1.000RIGHT      291388.21  86569.65RIGHT     4095      \n']
        
        self.unit_contents3 = \
        ['RIVER (Culvert Exit) CH:7932 - Trimmed to BT\n',
         'SECTION\n',
         '1.069\n',
         '    15.078            1.111111      1000\n',
         '        18\n',
         '     5.996    37.560     0.080     1.000LEFT       291391.67  86582.61LEFT      16        \n',
         '     6.936    37.197     0.035*    1.000           291391.43  86581.70          \n',
         '     7.446    36.726     0.035     1.000           291391.30  86581.21          \n',
         '     7.635    35.235     0.035     1.000           291391.25  86581.03          \n',
         '     8.561    35.196     0.035     1.000           291391.01  86580.13          \n',
         '     9.551    35.190     0.035     1.000BED        291390.75  86579.18          \n',
         '    10.323    35.229     0.035     1.000           291390.55  86578.43          \n',
         '    10.904    35.319     0.035     1.000           291390.40  86577.87          \n',
         '    12.542    35.637     0.035     1.000           291389.98  86576.29          \n',
         '    13.740    35.593     0.035     1.000           291389.67  86575.13          \n',
         '    13.788    35.592     0.035     1.000           291389.66  86575.09          \n',
         '    13.944    36.148     0.035     1.000           291389.62  86574.93          \n',
         '    15.008    36.559     0.080*    1.000           291389.34  86573.91          \n',
         '    16.355    37.542     0.080     1.000           291389.00  86572.60          \n',
         '    17.424    38.518     0.080     1.000           291388.72  86571.57          \n',
         '    18.449    39.037     0.080     1.000           291388.46  86570.58          \n',
         '    19.416    39.146     0.080     1.000           291388.21  86569.65          \n',
         '    19.420    39.133     0.080     1.000RIGHT      291388.21  86569.65RIGHT     4095      \n']
        
        self.unit_contents4 = \
        ['Baseline 1% AEP Run',
         '#REVISION#1',
         '        62     0.750     0.900     0.100     0.002        12',
         '    10.000     0.020     0.010     0.700     0.101     0.701     0.000',
         'RAD FILE',
         '..\\..\\..\\..\\..\\..\\..\\..\\rgh\\roughness.rad'
        ]
        
        # Use the unit factory to convert the text input into actual river units.
        factory = iuf()
        i, self.header = factory.createUnit(self.unit_contents4, 0, 'header', 1)
        i, self.river1 = factory.createUnit(self.unit_contents1, 0, 'river', 1, 1) 
        i, self.river2 = factory.createUnit(self.unit_contents2, 0, 'river', 2, 1) 
        i, self.river3 = factory.createUnit(self.unit_contents3, 0, 'river', 3, 1)
         

    def test_initialisedDat_method(self):
        """Make sure we're creating default setup collections properly."""
        
        # No units given to setup
        dat = DatCollection.initialisedDat(self.fake_path)
        self.assertTrue(dat[0].UNIT_TYPE == 'Header')
        self.assertTrue(dat[1].UNIT_TYPE == 'Comment')
        self.assertTrue(dat[2].UNIT_TYPE == 'Initial Conditions')
        
        # With units given to setup
        new_r = riverunit.RiverUnit(1)
        new_r.name = 'River1'
        new_r.addDataRow({ROW_DATA_TYPES.CHAINAGE: 0.000, ROW_DATA_TYPES.ELEVATION: 10.000}, index=0)
        new_r.addDataRow({ROW_DATA_TYPES.CHAINAGE: 5.000, ROW_DATA_TYPES.ELEVATION: 6.000}, index=1)
        new_r.addDataRow({ROW_DATA_TYPES.CHAINAGE: 10.000, ROW_DATA_TYPES.ELEVATION: 10.000}, index=2)
        new_r2 = riverunit.RiverUnit(1)
        new_r2.name = 'River2'
        new_r2.addDataRow({ROW_DATA_TYPES.CHAINAGE: 0.000, ROW_DATA_TYPES.ELEVATION: 8.000}, index=0)
        new_r2.addDataRow({ROW_DATA_TYPES.CHAINAGE: 5.000, ROW_DATA_TYPES.ELEVATION: 4.000}, index=1)
        new_r2.addDataRow({ROW_DATA_TYPES.CHAINAGE: 10.000, ROW_DATA_TYPES.ELEVATION: 8.000}, index=2)
        units = [new_r, new_r2]
        dat = DatCollection.initialisedDat(self.fake_path, units)
        self.assertTrue(dat[0].UNIT_TYPE == 'Header')
        self.assertTrue(dat[1].UNIT_TYPE == 'Comment')
        self.assertTrue(dat[2].UNIT_TYPE == 'River')
        self.assertTrue(dat[3].UNIT_TYPE == 'River')
        self.assertTrue(dat[4].UNIT_TYPE == 'Initial Conditions')


    def test_addUnit_method(self):
        '''Check what happens when we try and add a few units
        '''
        # Create a new IsisUnitCollection object
        dat = DatCollection.initialisedDat(self.fake_path)
        
        # Add a unit to the class
        dat.addUnit(self.river1, ics={ROW_DATA_TYPES.ELEVATION: 10.0, ROW_DATA_TYPES.FLOW: 3.0}) 
        
        # Check that it was successfully loaded into the collection
        self.assertTrue(dat.units[2].name == '1.067', 'addUnit Test - cannot retrieve name fail')
        
        # Make sure initial conditions have been updated
        ic = dat.getUnit('Initial Conditions')
        ic_label = ic.getRowDataAsList(ROW_DATA_TYPES.LABEL)
        ic_elev = ic.getRowDataAsList(ROW_DATA_TYPES.ELEVATION)
        ic_flow = ic.getRowDataAsList(ROW_DATA_TYPES.FLOW)
        self.assertListEqual(ic_label, ['1.067'], 'Initial conditions label update error')
        self.assertListEqual(ic_flow, [3.0], 'Initial conditions flow update error')
        self.assertListEqual(ic_elev, [10.0], 'Initial conditions elevation update error')
        
        # Make sure we can't put the wrong kind of object in there.
        redherring = {}
        self.assertRaises(AttributeError, lambda: dat.addUnit(redherring))
        
        self.assertEqual(dat.node_count, 1, 'Node counts not equal')
        
        
    def test_removeUnit_method(self):
        '''Make sure that we can safely remove units
        '''
        # Add a couple of units
#         dat = DatCollection(self.path_holder) 
        dat = DatCollection.initialisedDat(self.fake_path)
        dat.addUnit(self.river1)
        dat.addUnit(self.river2)
        
        # Remove a unit
        self.assertTrue(dat.removeUnit(self.river1.name, 'River'), 'Cannot remove river1 unit fail')
        
        # Make sure initial conditions have been updated
        ic = dat.getUnit('Initial Conditions')
        ic_label = ic.getRowDataAsList(ROW_DATA_TYPES.LABEL)
        self.assertListEqual(ic_label, ['1.068'], 'Initial conditions label update error')
        self.assertEqual(dat.node_count, 1)
        
        self.assertTrue(dat.removeUnit(self.river2.name, 'River'), 'Cannot remove river2 unit fail')
        self.assertFalse(dat.removeUnit(self.river1.name, 'River'), 'Remove non existing unit fail')
        self.assertEqual(dat.node_count, 0)


    def test_getPrintableContents(self):
        '''Ensure that the printable lists are in the format that we are
        expecting.
        '''
        # Make comparable out contents
        self.out_contents = \
        ['RIVER (Culvert Exit) CH:7932 - Trimmed to BT',
         'SECTION',
         '1.067',
         '    15.078            1.111111      1000',
         '        18',
         '     5.996    37.560     0.080     1.000LEFT       291391.67  86582.61LEFT      16        ',
         '     6.936    37.197     0.035*    1.000           291391.43  86581.70          ',
         '     7.446    36.726     0.035     1.000           291391.30  86581.21          ',
         '     7.635    35.235     0.035     1.000           291391.25  86581.03          ',
         '     8.561    35.196     0.035     1.000           291391.01  86580.13          ',
         '     9.551    35.190     0.035     1.000BED        291390.75  86579.18          ',
         '    10.323    35.229     0.035     1.000           291390.55  86578.43          ',
         '    10.904    35.319     0.035     1.000           291390.40  86577.87          ',
         '    12.542    35.637     0.035     1.000           291389.98  86576.29          ',
         '    13.740    35.593     0.035     1.000           291389.67  86575.13          ',
         '    13.788    35.592     0.035     1.000           291389.66  86575.09          ',
         '    13.944    36.148     0.035     1.000           291389.62  86574.93          ',
         '    15.008    36.559     0.080*    1.000           291389.34  86573.91          ',
         '    16.355    37.542     0.080     1.000           291389.00  86572.60          ',
         '    17.424    38.518     0.080     1.000           291388.72  86571.57          ',
         '    18.449    39.037     0.080     1.000           291388.46  86570.58          ',
         '    19.416    39.146     0.080     1.000           291388.21  86569.65          ',
         '    19.420    39.133     0.080     1.000RIGHT      291388.21  86569.65RIGHT     4095      ',
         'RIVER (Culvert Exit) CH:7932 - Trimmed to BT',
         'SECTION',
         '1.068',
         '    15.078            1.111111      1000',
         '        18',
         '     5.996    37.560     0.080     1.000LEFT       291391.67  86582.61LEFT      16        ',
         '     6.936    37.197     0.035*    1.000           291391.43  86581.70          ',
         '     7.446    36.726     0.035     1.000           291391.30  86581.21          ',
         '     7.635    35.235     0.035     1.000           291391.25  86581.03          ',
         '     8.561    35.196     0.035     1.000           291391.01  86580.13          ',
         '     9.551    35.190     0.035     1.000BED        291390.75  86579.18          ',
         '    10.323    35.229     0.035     1.000           291390.55  86578.43          ',
         '    10.904    35.319     0.035     1.000           291390.40  86577.87          ',
         '    12.542    35.637     0.035     1.000           291389.98  86576.29          ',
         '    13.740    35.593     0.035     1.000           291389.67  86575.13          ',
         '    13.788    35.592     0.035     1.000           291389.66  86575.09          ',
         '    13.944    36.148     0.035     1.000           291389.62  86574.93          ',
         '    15.008    36.559     0.080*    1.000           291389.34  86573.91          ',
         '    16.355    37.542     0.080     1.000           291389.00  86572.60          ',
         '    17.424    38.518     0.080     1.000           291388.72  86571.57          ',
         '    18.449    39.037     0.080     1.000           291388.46  86570.58          ',
         '    19.416    39.146     0.080     1.000           291388.21  86569.65          ',
         '    19.420    39.133     0.080     1.000RIGHT      291388.21  86569.65RIGHT     4095      ']
        
        # Add a couple of units
        col = DatCollection(self.path_holder)
        col.addUnit(self.river1, update_node_count=False)
        col.addUnit(self.river2, update_node_count=False)
        
        # Get the printable units from the collection
        print_unit = col.getPrintableContents()
        
        # Make sure the printed units are what we expect
        self.assertListEqual(self.out_contents, print_unit, 'GetPrintable units fail')
        

    def test_getUnitsByCategory(self):
        '''Checks that we can safely return units by category.
        '''
        # Add some units to the collection
        col = DatCollection(self.path_holder)
        col.addUnit(self.river1, update_node_count=False)
        col.addUnit(self.river2, update_node_count=False)
        col.addUnit(self.header, update_node_count=False)
        
        # Get the river units.
        river_cat = col.getUnitsByCategory('River')
        # Make sure we have the number that we think we should have
        self.assertTrue(len(river_cat) == 2, 'Number of river units fail')

        # Get the head unit
        header_cat = col.getUnitsByCategory('Meta')
        # Check that we only have one
        self.assertTrue(len(header_cat) == 1, 'Number of header units fail')
        
        # Try a non existent category
        non_cat = col.getUnitsByCategory('redherring')
        self.assertFalse(non_cat, 'Number of red herring units fail')
        
        
    def test_getUnit_method(self):
        '''Check we can safely get units by name.
        '''
        # Add some units to the collection
        col = DatCollection(self.path_holder)
        col.addUnit(self.river1, update_node_count=False)
        col.addUnit(self.river2, update_node_count=False)
        col.addUnit(self.header, update_node_count=False)
        
        # Get the unit we want
        river_unit = col.getUnit('1.067')
        
        # Make sure that it's right.
        self.assertTrue(river_unit.name == '1.067', 'Get River unit by name fail')
        
        # Get the header unit.
        header_unit = col.getUnit('Header')
        
        # Check it.
        self.assertTrue(header_unit.name == 'Header', 'Get header unit by name fail')
        
        # Remove all the units
        for u in col.units:
            del u
        
        # Make sure we got nothing
        no_unit = col.getUnit('River')
        self.assertFalse(no_unit, 'Get non existent unit fail')
        
        
        
    def test_getNoOfUnits_method(self):
        '''Make sure that it's returning the correct number of units.
        '''
        # Add some units to the collection
        col = DatCollection(self.path_holder)
        col.addUnit(self.river1, update_node_count=False)
        col.addUnit(self.river2, update_node_count=False)
        col.addUnit(self.header, update_node_count=False)
    
        # Get the number of units
        no_units = col.getNoOfUnits()
        
        # check that it's correct.
        self.assertTrue(no_units == 3, 'Get number of units fail')
    
    