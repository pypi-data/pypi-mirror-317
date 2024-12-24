import numpy as np
import pytest

from dynasor.post_processing import NeutronScatteringLengths, \
        XRayFormFactors, Weights, get_weighted_sample


def test_weigting_with_unity_weights(dynamic_sample_with_incoh):
    """Set all weights to 1, should get back initial structure factors"""
    weights_coh = {'A': 1.0, 'B': 1.0}
    weights_incoh = {'A': 1.0, 'B': 1.0}
    weights = Weights(weights_coh, weights_incoh)

    sample = dynamic_sample_with_incoh
    sample_weighted = get_weighted_sample(sample, weights)

    # compare correlation functions
    for key in sample.available_correlation_functions:
        expected = sample[key]
        computed = sample_weighted[key]
        assert np.allclose(expected, computed)

    # compare simulation parameters
    assert sample.atom_types == sample_weighted.atom_types
    assert sample.pairs == sample_weighted.pairs
    assert sample.particle_counts == sample_weighted.particle_counts
    assert np.allclose(sample.cell, sample_weighted.cell)
    assert sorted(sample.meta_data.keys()) == sorted(sample_weighted.meta_data.keys())
    assert sorted(sample._data_keys) == sorted(sample_weighted._data_keys)

    # Check that initial keys (such as q_points, time and omega) are copied.
    for key in sample.dimensions:
        assert np.allclose(sample[key], sample_weighted[key])


def test_weigting_with_zero_weights(dynamic_sample_with_incoh):
    """Set all weights to 0.0, all resulting structure factors should be zero"""
    weights_coh = {'A': 0.0, 'B': 0.0}
    weights_incoh = {'A': 0.0, 'B': 0.0}
    weights = Weights(weights_coh, weights_incoh)

    sample = dynamic_sample_with_incoh
    sample_weighted = get_weighted_sample(sample, weights)

    # compare correlation functions
    for key in sample.available_correlation_functions:
        computed = sample_weighted[key]
        expected = np.zeros(computed.shape)
        assert np.allclose(expected, computed)

    # compare simulation parameters
    assert sample.atom_types == sample_weighted.atom_types
    assert sample.pairs == sample_weighted.pairs
    assert sample.particle_counts == sample_weighted.particle_counts
    assert np.allclose(sample.cell, sample_weighted.cell)
    assert sorted(sample.meta_data.keys()) == sorted(sample_weighted.meta_data.keys())
    assert sorted(sample._data_keys) == sorted(sample_weighted._data_keys)

    # Check that initial keys (such as q_points, time and omega) are copied.
    for key in sample.dimensions:
        assert np.allclose(sample[key], sample_weighted[key])


def test_weigting_with_real_weights(dynamic_sample_with_incoh):
    weights_coh = {'A': 2.792, 'B': 5.43}
    weights_incoh = {'A': 12.89, 'B': 74.222}
    weights = Weights(weights_coh, weights_incoh)

    sample = dynamic_sample_with_incoh
    sample_weighted = get_weighted_sample(sample, weights)

    # compare coherent correlation functions
    names = ['Fqt_coh', 'Sqw_coh', 'Clqt', 'Clqw', 'Ctqt', 'Ctqw']
    pairs = [('A', 'A'), ('A', 'B'), ('B', 'B')]
    for name in names:
        # check partials
        expected_total = np.zeros(sample.Fqt_coh.shape)
        for atom_type1, atom_type2 in pairs:
            key = f'{name}_{atom_type1}_{atom_type2}'
            expected = weights_coh[atom_type1] * weights_coh[atom_type2] * sample[key]
            expected_total += expected
            assert np.allclose(expected, sample_weighted[key])
        # check total
        assert np.allclose(expected_total, sample_weighted[name])

    # compare incoherent correlation functions
    names = ['Fqt_incoh', 'Sqw_incoh']
    atom_types = ['A', 'B']
    for name in names:
        # check partials
        expected_total = np.zeros(sample.Fqt_incoh.shape)
        for atom_type in atom_types:
            key = f'{name}_{atom_type}'
            expected = weights_incoh[atom_type] * sample[key]
            expected_total += expected
            assert np.allclose(expected, sample_weighted[key])
        # check total
        assert np.allclose(expected_total, sample_weighted[name])

    # compare simulation parameters
    assert sample.atom_types == sample_weighted.atom_types
    assert sample.pairs == sample_weighted.pairs
    assert sample.particle_counts == sample_weighted.particle_counts
    assert np.allclose(sample.cell, sample_weighted.cell)
    assert sorted(sample.meta_data.keys()) == sorted(sample_weighted.meta_data.keys())
    assert sorted(sample._data_keys) == sorted(sample_weighted._data_keys)

    # Check that initial keys (such as q_points, time and omega) are copied.
    for key in sample.dimensions:
        assert np.allclose(sample[key], sample_weighted[key])


def test_weigting_with_real_weights_without_incoh(dynamic_sample_without_incoh):
    weights_coh = {'A': -12.792, 'B': 45.43}
    weights = Weights(weights_coh)

    sample = dynamic_sample_without_incoh
    sample_weighted = get_weighted_sample(sample, weights)

    # compare coherent correlation functions
    names = ['Fqt_coh', 'Sqw_coh', 'Clqt', 'Clqw', 'Ctqt', 'Ctqw']
    pairs = [('A', 'A'), ('A', 'B'), ('B', 'B')]
    for name in names:
        # check partials
        expected_total = np.zeros(sample.Fqt_coh.shape)
        for atom_type1, atom_type2 in pairs:
            key = f'{name}_{atom_type1}_{atom_type2}'
            expected = weights_coh[atom_type1] * weights_coh[atom_type2] * sample[key]
            expected_total += expected
            assert np.allclose(expected, sample_weighted[key])
        # check total
        assert np.allclose(expected_total, sample_weighted[name])


def test_weighting_of_static_sample(static_sample):
    weights_coh = {'A': 22.1, 'B': 5}
    weights = Weights(weights_coh)

    sample = static_sample
    sample_weighted = get_weighted_sample(sample, weights)

    # compare partial Sq
    name = 'Sq'
    pairs = [('A', 'A'), ('A', 'B'), ('B', 'B')]
    expected_total = np.zeros(sample.Sq.shape)
    for atom_type1, atom_type2 in pairs:
        key = f'{name}_{atom_type1}_{atom_type2}'
        expected = weights_coh[atom_type1] * weights_coh[atom_type2] * sample[key]
        expected_total += expected
        assert np.allclose(expected, sample_weighted[key])

    # check total
    assert np.allclose(expected_total, sample_weighted[name])


def test_weighting_without_incoh_weights(dynamic_sample_with_incoh):
    """ check that weighting where weights does not support incoh works as expected """
    weights_coh = {'A': 2.792, 'B': 5.43}
    weights = Weights(weights_coh)

    with pytest.warns(UserWarning):
        sample_weighted = get_weighted_sample(dynamic_sample_with_incoh, weights)

    expected_keys = ['Fqt_coh', 'Fqt_coh_A_A', 'Fqt_coh_A_B', 'Fqt_coh_B_B', 'Fqt',
                     'Sqw_coh', 'Sqw_coh_A_A', 'Sqw_coh_A_B', 'Sqw_coh_B_B', 'Sqw',
                     'Clqt', 'Clqt_A_A', 'Clqt_A_B', 'Clqt_B_B',
                     'Clqw', 'Clqw_A_A', 'Clqw_A_B', 'Clqw_B_B',
                     'Ctqt', 'Ctqt_A_A', 'Ctqt_A_B', 'Ctqt_B_B',
                     'Ctqw', 'Ctqw_A_A', 'Ctqw_A_B', 'Ctqw_B_B']
    assert sorted(sample_weighted.available_correlation_functions) == sorted(expected_keys)
    assert sorted(sample_weighted.dimensions) == ['omega', 'q_points', 'time']

    keys_not_expected = ['Fqt_incoh', 'Fqt_incoh_A_A', 'Fqt_incoh_A_B', 'Fqt_incoh_B_B',
                         'Sqw_incoh', 'Sqw_incoh_A_A', 'Sqw_incoh_A_B', 'Sqw_incoh_B_B']
    for key in keys_not_expected:
        assert key not in sample_weighted.available_correlation_functions
        assert key not in sample_weighted._data_keys


def test_weighting_without_current_support(dynamic_sample_without_incoh):
    """ check that weighting where weights does not support currents works as expected """
    weights_coh = {'A': 2.792, 'B': 5.43}
    weights_incoh = {'A': 12.89, 'B': 74.222}
    weights = Weights(weights_coh, weights_incoh, supports_currents=False)

    with pytest.warns(UserWarning):
        sample_weighted = get_weighted_sample(dynamic_sample_without_incoh, weights)

    expected_keys = ['Fqt_coh', 'Fqt_coh_A_A', 'Fqt_coh_A_B', 'Fqt_coh_B_B', 'Fqt',
                     'Sqw_coh', 'Sqw_coh_A_A', 'Sqw_coh_A_B', 'Sqw_coh_B_B', 'Sqw']
    assert sorted(sample_weighted.available_correlation_functions) == sorted(expected_keys)
    assert sorted(sample_weighted.dimensions) == ['omega', 'q_points', 'time']


# Neutron weights
@pytest.mark.parametrize('species,b_coh,b_inc', [
    (['H'], {'H': -3.73904}, {'H': 25.27081**2}),
    (['C', 'O'], {'C': 6.64603, 'O': 5.80307}, {'C': (-0.00572)**2, 'O': 0.0000684**2}),
    ])
def test_neutron_scattering_lengths_isotope_average(species, b_coh, b_inc):
    """
    Ensure that the isotope average scattering lengths
    matches the NIST table:
    https://www.ncnr.nist.gov/resources/n-lengths/list.html
    """
    weights = NeutronScatteringLengths(species)

    for s in species:
        assert np.isclose(weights.get_weight_coh(s), b_coh[s])
        assert np.isclose(weights.get_weight_incoh(s), b_inc[s])


@pytest.mark.parametrize('species,b_coh,b_inc,abundance', [
    (['H'], {'H': 2.53994}, {'H': 9.16762**2}, {'H': {1: 0.33, 2: 0.30, 3: 0.37}}),
    (
        ['C', 'O'], {'C': 6.32833, 'O': 5.81575}, {'C': (-0.364)**2, 'O': 0.045**2},
        {'C': {12: 0.3, 13: 0.7}, 'O': {16: 0.25, 17: 0.25, 18: 0.5}}
     ),
    ])
def test_neutron_scattering_lengths_custom_abundance(species, b_coh, b_inc, abundance):
    """Make sure abundance weighting works as intended."""
    weights = NeutronScatteringLengths(species, abundance)

    for s in species:
        assert np.isclose(weights.get_weight_coh(s), b_coh[s])
        assert np.isclose(weights.get_weight_incoh(s), b_inc[s])

    # Fetch the abundances and make sure they match
    for species, abs in abundance.items():
        assert abs == weights.abundances[species]


@pytest.mark.parametrize('species,abundance,should_raise', [
        (['K'], None, True),
        (['K'], {'K': {39: 0.93, 40: 0, 41: 0.07}}, False)
    ])
def test_neutron_scattering_lengths_missing_in_database(species, abundance, should_raise):
    """Should throw a value error when requested species has missing data in the database."""
    if should_raise:
        with pytest.raises(ValueError) as e:
            NeutronScatteringLengths(species, abundance)
        assert 'Non-zero abundance of 40K' in str(e)
    else:
        NeutronScatteringLengths(species, abundance)


def test_neutron_scattering_lengths_invalid_total_abundance():
    """Should throw a value error when the abundances does not add up to 1.0 for each species"""
    abundance = {'O': {16: 0.3, 17: 0.8, 18: 0.0}, 'N': {14: 0.8, 15: 0.2}}
    with pytest.raises(ValueError) as e:
        NeutronScatteringLengths(['O', 'N'], abundance)
    assert 'Abundance values for O do not sum up to 1.0' in str(e)


def test_neutron_scattering_lengths_invalid_isotope_in_abundance():
    """Should throw a value error when the selected isotope does not exist"""
    abundance = {'V': {10: 1.0}}
    with pytest.raises(ValueError) as e:
        NeutronScatteringLengths(['V'], abundance)
    assert 'No match in database for V and isotope 10' in str(e)


# X-ray weights
@pytest.mark.parametrize('species,q_norm,method', [
    (['He'], np.array([1, 2, 3]), 'waasmaier-1995'),
    (['C', 'O'], np.array([1, 2, 3, 0.5999]).reshape(-1, 1), 'waasmaier-1995'),
    (['Sb3+', 'O1-'], np.array([0.1, 0.2]), 'waasmaier-1995')
    ])
def test_xray_form_factors_shapes(species, q_norm, method):
    weights = XRayFormFactors(species, method)
    for s in species:
        for q in q_norm:
            coh = weights.get_weight_coh(s, q)
            incoh = weights.get_weight_incoh(s, q)
            assert incoh is None
            assert coh.shape is not None


@pytest.mark.parametrize('species,q_norm,method,result', [
        (['He'], np.array([1, 2]), 'waasmaier-1995', [0.09539912837127983, 0.0097169894132503]),
        (['O'], np.array([1, 2]), 'waasmaier-1995', [1.3770183528975948, 0.6732633649895161]),
    ])
def test_xray_form_factors_numeric(species, q_norm, method, result):
    """
    Manually compute f0 from the given source and check that the numbers match.
    Note that this does not guarantee that no errors have been made in OCR:ing
    the tables; it just serves as a spot-check.
    """
    q_norm = np.array(q_norm)*4*np.pi  # updated the definition of s after computing ref values.
    weights = XRayFormFactors(species, method)
    for s in species:
        for q, expected in zip(q_norm, result):
            coh = weights.get_weight_coh(s, q)
            assert np.isclose(coh, expected)


@pytest.mark.parametrize('species,q_norm,method', [
    (['H+'], np.array([1, 2, 3]), 'waasmaier-1995'),
    (['C-', 'O5+'], np.array([1, 2, 3]), 'waasmaier-1995'),
    (['H+', 'C'], np.array([0.1, 0.05, 2]), 'waasmaier-1995'),
    ])
def test_xray_form_factors_invalid_species(species, q_norm, method):
    """
    Some or all of the species are missing from the requested database.
    Should raise an error when missing species are requested.
    """
    with pytest.raises(ValueError) as e:
        XRayFormFactors(species, method)
    assert f'Missing tabulated values for requested species {species[0]}' in str(e)


@pytest.mark.parametrize('species,q_norm,method', [
    (['H'], np.array([1, 2, 3]), 'waasmaier-1995'),
    (['H', 'C'], np.array([0.1, 0.05, 2]), 'waasmaier-1995'),
    ])
def test_xray_form_factors_sets_hydrogen_to_zero(species, q_norm, method):
    """
    Some or all of the species are missing from the requested database.
    Should raise an error when missing species are requested.
    """
    warning = 'No parametrization for H. Setting form factor for H to zero'
    with pytest.warns(UserWarning, match=warning):
        weights = XRayFormFactors(species, method)
    weight_H = weights.get_weight_coh(species[0], q_norm[0])
    assert weight_H == 0.0


@pytest.mark.parametrize('species,q_norm,method,error', [
    (['He'], None, 'waasmaier-1995', 'missing 1 required positional argument'),
    (['He'], np.array([100]), 'waasmaier-1995',
     'Waasmaier parametrization is not reliable')
])
def test_xray_form_factors_invalid_q_norm(species, q_norm, method, error):

    """
    Some or all of the species are missing from the requested database.
    Should raise an error when missing species are requested.
    """
    weights = XRayFormFactors(species, method)
    if q_norm is None:
        with pytest.raises(TypeError) as e:
            weights.get_weight_coh(species[0])
        assert error in str(e)
    else:
        with pytest.warns(UserWarning, match=error):
            weights.get_weight_coh(species[0], q_norm[0])


# TODO integration tests for X-rays, neutrons and electrons
@pytest.mark.parametrize('sample_with_species,probe', [
    (['He', 'C'], 'neutrons'),
    (['He', 'C'], 'xrays'),
    (['He', 'C'], 'electrons')
], indirect=['sample_with_species'])
def test_weighting_integration_test(sample_with_species, probe):
    """
    Integration test where a mock sample is weighted by actual
    probe specific weights.
    """
    species = sample_with_species.atom_types
    atom_type = species[0]
    sqw = f'Sqw_coh_{atom_type}_{atom_type}'
    unweighted = sample_with_species[sqw]
    if probe == 'neutrons':
        weights = NeutronScatteringLengths(species)
        # The quotient between the unweighted and weighted Sqw for the first
        # species should be the scattering length for that species, for all
        # q_values.
        bi = weights.get_weight_coh(atom_type)
        scattering_length = np.ones(unweighted.shape)*bi**2
        expected = scattering_length

    elif probe == 'xrays':
        weights = XRayFormFactors(species, source='waasmaier-1995')
        # The quotient now depends on the norm of q.
        # Compute q_norm, and the prepare the expected
        # form factors.
        q_norms = np.linalg.norm(sample_with_species.q_points, axis=1)
        form_factors = np.reshape([weights.get_weight_coh(atom_type, q) for q in q_norms], (-1, 1))
        expected = form_factors**2
    elif probe == 'electrons':
        # TODO
        return
    with pytest.warns(UserWarning, match='The Weights does not support'):
        weighted_sample = get_weighted_sample(sample_with_species, weights)

    weighted = weighted_sample[sqw]
    quotient = weighted / unweighted
    assert np.allclose(quotient, expected)
