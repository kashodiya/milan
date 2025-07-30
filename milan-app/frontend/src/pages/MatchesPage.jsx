





import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Button,
  Chip,
  CircularProgress,
  TextField,
  InputAdornment,
  IconButton,
  Pagination,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Divider,
  Alert
} from '@mui/material';
import { Search as SearchIcon, Favorite, Message, PersonAdd } from '@mui/icons-material';
import { matchService, connectionService } from '../services/api';
import { useAuth } from '../context/AuthContext';

const MatchesPage = () => {
  const { currentUser } = useAuth();
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCriteria, setFilterCriteria] = useState({
    religion: '',
    marital_status: '',
    location: '',
  });
  const [sentInterests, setSentInterests] = useState({});
  const [interestLoading, setInterestLoading] = useState({});
  const matchesPerPage = 10;

  useEffect(() => {
    fetchMatches();
  }, [page]);

  const fetchMatches = async () => {
    setLoading(true);
    setError(null);
    try {
      const skip = (page - 1) * matchesPerPage;
      const response = await matchService.findMatches(skip, matchesPerPage);
      setMatches(response.data);
      
      // Get connections to check if interest already sent
      const connectionsResponse = await connectionService.getMyConnections();
      const connections = connectionsResponse.data;
      
      // Create a map of user_id -> connection status
      const interestMap = {};
      connections.forEach(conn => {
        if (conn.sender_id === currentUser.user_id) {
          interestMap[conn.receiver_id] = conn.status;
        }
      });
      
      setSentInterests(interestMap);
    } catch (err) {
      console.error('Error fetching matches:', err);
      setError(err.response?.data?.detail || 'Failed to load matches. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const handleSendInterest = async (userId) => {
    setInterestLoading(prev => ({ ...prev, [userId]: true }));
    try {
      await connectionService.sendInterest(userId);
      setSentInterests(prev => ({ ...prev, [userId]: 'pending' }));
    } catch (err) {
      console.error('Error sending interest:', err);
    } finally {
      setInterestLoading(prev => ({ ...prev, [userId]: false }));
    }
  };

  const handlePageChange = (event, value) => {
    setPage(value);
  };

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilterCriteria(prev => ({ ...prev, [name]: value }));
  };

  const resetFilters = () => {
    setSearchTerm('');
    setFilterCriteria({
      religion: '',
      marital_status: '',
      location: '',
    });
  };

  // Filter matches based on search term and filters
  const filteredMatches = matches.filter(match => {
    const fullName = `${match.first_name} ${match.last_name}`.toLowerCase();
    const searchMatch = searchTerm === '' || fullName.includes(searchTerm.toLowerCase());
    
    const religionMatch = filterCriteria.religion === '' || match.religion === filterCriteria.religion;
    const maritalMatch = filterCriteria.marital_status === '' || match.marital_status === filterCriteria.marital_status;
    const locationMatch = filterCriteria.location === '' || 
                         match.location_city.includes(filterCriteria.location) || 
                         match.location_state.includes(filterCriteria.location) || 
                         match.location_country.includes(filterCriteria.location);
    
    return searchMatch && religionMatch && maritalMatch && locationMatch;
  });

  // Calculate age from date of birth
  const calculateAge = (dateOfBirth) => {
    const today = new Date();
    const birthDate = new Date(dateOfBirth);
    let age = today.getFullYear() - birthDate.getFullYear();
    const monthDiff = today.getMonth() - birthDate.getMonth();
    
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
      age--;
    }
    
    return age;
  };

  if (loading && page === 1) {
    return (
      <Container sx={{ textAlign: 'center', py: 5 }}>
        <CircularProgress />
        <Typography sx={{ mt: 2 }}>Loading matches...</Typography>
      </Container>
    );
  }

  return (
    <Container>
      <Typography variant="h4" component="h1" gutterBottom sx={{ mt: 3 }}>
        Find Your Match
      </Typography>
      
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}
      
      {/* Search and Filter Section */}
      <Box sx={{ mb: 4, p: 2, bgcolor: 'background.paper', borderRadius: 1 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              label="Search by Name"
              variant="outlined"
              value={searchTerm}
              onChange={handleSearchChange}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon />
                  </InputAdornment>
                ),
              }}
            />
          </Grid>
          <Grid item xs={12} md={8}>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={4}>
                <FormControl fullWidth variant="outlined">
                  <InputLabel>Religion</InputLabel>
                  <Select
                    name="religion"
                    value={filterCriteria.religion}
                    onChange={handleFilterChange}
                    label="Religion"
                  >
                    <MenuItem value="">Any</MenuItem>
                    <MenuItem value="Hindu">Hindu</MenuItem>
                    <MenuItem value="Muslim">Muslim</MenuItem>
                    <MenuItem value="Christian">Christian</MenuItem>
                    <MenuItem value="Sikh">Sikh</MenuItem>
                    <MenuItem value="Buddhist">Buddhist</MenuItem>
                    <MenuItem value="Jain">Jain</MenuItem>
                    <MenuItem value="Other">Other</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={4}>
                <FormControl fullWidth variant="outlined">
                  <InputLabel>Marital Status</InputLabel>
                  <Select
                    name="marital_status"
                    value={filterCriteria.marital_status}
                    onChange={handleFilterChange}
                    label="Marital Status"
                  >
                    <MenuItem value="">Any</MenuItem>
                    <MenuItem value="never_married">Never Married</MenuItem>
                    <MenuItem value="divorced">Divorced</MenuItem>
                    <MenuItem value="widowed">Widowed</MenuItem>
                    <MenuItem value="separated">Separated</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={4}>
                <TextField
                  fullWidth
                  label="Location"
                  variant="outlined"
                  name="location"
                  value={filterCriteria.location}
                  onChange={handleFilterChange}
                />
              </Grid>
            </Grid>
          </Grid>
          <Grid item xs={12} sx={{ display: 'flex', justifyContent: 'flex-end' }}>
            <Button variant="outlined" onClick={resetFilters} sx={{ mr: 1 }}>
              Reset Filters
            </Button>
            <Button variant="contained" onClick={fetchMatches}>
              Apply Filters
            </Button>
          </Grid>
        </Grid>
      </Box>
      
      {/* Results Section */}
      {filteredMatches.length > 0 ? (
        <Grid container spacing={3}>
          {filteredMatches.map((match) => (
            <Grid item xs={12} sm={6} md={4} key={match.user_id}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <CardMedia
                  component="img"
                  height="200"
                  image={match.profile_photo || 'https://via.placeholder.com/200x200?text=No+Photo'}
                  alt={`${match.first_name} ${match.last_name}`}
                />
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography variant="h6" component="div" gutterBottom>
                    {match.first_name} {match.last_name}, {calculateAge(match.date_of_birth)}
                  </Typography>
                  <Box sx={{ mb: 1 }}>
                    <Chip 
                      size="small" 
                      label={match.religion || 'Not specified'} 
                      sx={{ mr: 0.5, mb: 0.5 }} 
                    />
                    <Chip 
                      size="small" 
                      label={match.marital_status.replace('_', ' ')} 
                      sx={{ mr: 0.5, mb: 0.5 }} 
                    />
                  </Box>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    {match.occupation || 'Occupation not specified'}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    {match.education || 'Education not specified'}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {[match.location_city, match.location_state, match.location_country]
                      .filter(Boolean)
                      .join(', ')}
                  </Typography>
                </CardContent>
                <Divider />
                <Box sx={{ p: 2, display: 'flex', justifyContent: 'space-between' }}>
                  <Button 
                    component={Link} 
                    to={`/profile/${match.user_id}`}
                    size="small"
                  >
                    View Profile
                  </Button>
                  {sentInterests[match.user_id] ? (
                    <Chip 
                      label={sentInterests[match.user_id] === 'accepted' ? 'Connected' : 'Interest Sent'} 
                      color={sentInterests[match.user_id] === 'accepted' ? 'success' : 'primary'} 
                      size="small" 
                    />
                  ) : (
                    <Button
                      size="small"
                      variant="outlined"
                      color="primary"
                      startIcon={<Favorite />}
                      onClick={() => handleSendInterest(match.user_id)}
                      disabled={interestLoading[match.user_id]}
                    >
                      {interestLoading[match.user_id] ? 'Sending...' : 'Send Interest'}
                    </Button>
                  )}
                </Box>
              </Card>
            </Grid>
          ))}
        </Grid>
      ) : (
        <Box sx={{ textAlign: 'center', py: 5 }}>
          <Typography variant="h6" gutterBottom>
            No matches found
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Try adjusting your search criteria or update your preferences.
          </Typography>
        </Box>
      )}
      
      {/* Pagination */}
      {matches.length > 0 && (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4, mb: 2 }}>
          <Pagination 
            count={Math.ceil(matches.length / matchesPerPage)} 
            page={page} 
            onChange={handlePageChange} 
            color="primary" 
          />
        </Box>
      )}
    </Container>
  );
};

export default MatchesPage;





