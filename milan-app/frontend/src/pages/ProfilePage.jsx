




import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Grid,
  TextField,
  Button,
  Paper,
  Tabs,
  Tab,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  Snackbar,
  Alert,
  Avatar,
  IconButton,
  Card,
  CardMedia,
  CardActions
} from '@mui/material';
import { PhotoCamera, Delete } from '@mui/icons-material';
import { useAuth } from '../context/AuthContext';
import { profileService, photoService, preferenceService, familyService } from '../services/api';

// Tab Panel Component
function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`profile-tabpanel-${index}`}
      aria-labelledby={`profile-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

const ProfilePage = () => {
  const { currentUser } = useAuth();
  const navigate = useNavigate();
  const [tabValue, setTabValue] = useState(0);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [notification, setNotification] = useState({ open: false, message: '', severity: 'success' });
  
  // Profile state
  const [profile, setProfile] = useState({
    first_name: '',
    last_name: '',
    gender: '',
    date_of_birth: '',
    height: '',
    religion: '',
    caste: '',
    mother_tongue: '',
    marital_status: '',
    about_me: '',
    occupation: '',
    education: '',
    income_bracket: '',
    location_city: '',
    location_state: '',
    location_country: '',
  });
  
  // Photos state
  const [photos, setPhotos] = useState([]);
  const [uploadingPhoto, setUploadingPhoto] = useState(false);
  
  // Preferences state
  const [preferences, setPreferences] = useState({
    min_age: '',
    max_age: '',
    height_min: '',
    height_max: '',
    religion: '',
    caste_preferences: '',
    education_level: '',
    income_min: '',
    location_preferences: '',
    other_preferences: '',
  });
  
  // Family details state
  const [familyDetails, setFamilyDetails] = useState({
    father_occupation: '',
    mother_occupation: '',
    siblings_count: '',
    family_type: '',
    family_values: '',
    about_family: '',
  });

  useEffect(() => {
    if (!currentUser) {
      navigate('/login');
      return;
    }
    
    const fetchProfileData = async () => {
      setLoading(true);
      try {
        // Try to fetch profile
        try {
          const profileResponse = await profileService.getMyProfile();
          setProfile(profileResponse.data);
        } catch (error) {
          if (error.response?.status !== 404) {
            console.error('Error fetching profile:', error);
          }
        }
        
        // Try to fetch photos
        try {
          const photosResponse = await photoService.getMyPhotos();
          setPhotos(photosResponse.data);
        } catch (error) {
          if (error.response?.status !== 404) {
            console.error('Error fetching photos:', error);
          }
        }
        
        // Try to fetch preferences
        try {
          const preferencesResponse = await preferenceService.getMyPreferences();
          setPreferences(preferencesResponse.data);
        } catch (error) {
          if (error.response?.status !== 404) {
            console.error('Error fetching preferences:', error);
          }
        }
        
        // Try to fetch family details
        try {
          const familyResponse = await familyService.getMyFamilyDetails();
          setFamilyDetails(familyResponse.data);
        } catch (error) {
          if (error.response?.status !== 404) {
            console.error('Error fetching family details:', error);
          }
        }
      } finally {
        setLoading(false);
      }
    };
    
    fetchProfileData();
  }, [currentUser, navigate]);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleProfileChange = (e) => {
    const { name, value } = e.target;
    setProfile(prev => ({ ...prev, [name]: value }));
  };

  const handlePreferencesChange = (e) => {
    const { name, value } = e.target;
    setPreferences(prev => ({ ...prev, [name]: value }));
  };

  const handleFamilyChange = (e) => {
    const { name, value } = e.target;
    setFamilyDetails(prev => ({ ...prev, [name]: value }));
  };

  const handlePhotoUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    setUploadingPhoto(true);
    try {
      const isPrimary = photos.length === 0; // First photo is primary
      await photoService.uploadPhoto(file, isPrimary);
      
      // Refresh photos
      const photosResponse = await photoService.getMyPhotos();
      setPhotos(photosResponse.data);
      
      setNotification({
        open: true,
        message: 'Photo uploaded successfully',
        severity: 'success'
      });
    } catch (error) {
      console.error('Error uploading photo:', error);
      setNotification({
        open: true,
        message: 'Failed to upload photo',
        severity: 'error'
      });
    } finally {
      setUploadingPhoto(false);
    }
  };

  const handleDeletePhoto = async (photoId) => {
    try {
      await photoService.deletePhoto(photoId);
      
      // Refresh photos
      const photosResponse = await photoService.getMyPhotos();
      setPhotos(photosResponse.data);
      
      setNotification({
        open: true,
        message: 'Photo deleted successfully',
        severity: 'success'
      });
    } catch (error) {
      console.error('Error deleting photo:', error);
      setNotification({
        open: true,
        message: 'Failed to delete photo',
        severity: 'error'
      });
    }
  };

  const saveProfile = async () => {
    setSaving(true);
    try {
      if (profile.profile_id) {
        await profileService.updateProfile(profile);
      } else {
        await profileService.createProfile(profile);
      }
      
      setNotification({
        open: true,
        message: 'Profile saved successfully',
        severity: 'success'
      });
    } catch (error) {
      console.error('Error saving profile:', error);
      setNotification({
        open: true,
        message: 'Failed to save profile',
        severity: 'error'
      });
    } finally {
      setSaving(false);
    }
  };

  const savePreferences = async () => {
    setSaving(true);
    try {
      if (preferences.preference_id) {
        await preferenceService.updatePreferences(preferences);
      } else {
        await preferenceService.createPreferences(preferences);
      }
      
      setNotification({
        open: true,
        message: 'Preferences saved successfully',
        severity: 'success'
      });
    } catch (error) {
      console.error('Error saving preferences:', error);
      setNotification({
        open: true,
        message: 'Failed to save preferences',
        severity: 'error'
      });
    } finally {
      setSaving(false);
    }
  };

  const saveFamilyDetails = async () => {
    setSaving(true);
    try {
      if (familyDetails.family_id) {
        await familyService.updateFamilyDetails(familyDetails);
      } else {
        await familyService.createFamilyDetails(familyDetails);
      }
      
      setNotification({
        open: true,
        message: 'Family details saved successfully',
        severity: 'success'
      });
    } catch (error) {
      console.error('Error saving family details:', error);
      setNotification({
        open: true,
        message: 'Failed to save family details',
        severity: 'error'
      });
    } finally {
      setSaving(false);
    }
  };

  const handleCloseNotification = () => {
    setNotification({ ...notification, open: false });
  };

  if (loading) {
    return (
      <Container>
        <Typography>Loading profile...</Typography>
      </Container>
    );
  }

  return (
    <Container>
      <Paper sx={{ mt: 3, mb: 3 }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="profile tabs">
            <Tab label="Basic Info" />
            <Tab label="Photos" />
            <Tab label="Partner Preferences" />
            <Tab label="Family Details" />
          </Tabs>
        </Box>
        
        {/* Basic Info Tab */}
        <TabPanel value={tabValue} index={0}>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="First Name"
                name="first_name"
                value={profile.first_name || ''}
                onChange={handleProfileChange}
                required
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Last Name"
                name="last_name"
                value={profile.last_name || ''}
                onChange={handleProfileChange}
                required
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth required>
                <InputLabel>Gender</InputLabel>
                <Select
                  name="gender"
                  value={profile.gender || ''}
                  label="Gender"
                  onChange={handleProfileChange}
                >
                  <MenuItem value="male">Male</MenuItem>
                  <MenuItem value="female">Female</MenuItem>
                  <MenuItem value="other">Other</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Date of Birth"
                name="date_of_birth"
                type="date"
                value={profile.date_of_birth || ''}
                onChange={handleProfileChange}
                InputLabelProps={{ shrink: true }}
                required
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Height (cm)"
                name="height"
                type="number"
                value={profile.height || ''}
                onChange={handleProfileChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Religion"
                name="religion"
                value={profile.religion || ''}
                onChange={handleProfileChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Caste"
                name="caste"
                value={profile.caste || ''}
                onChange={handleProfileChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Mother Tongue"
                name="mother_tongue"
                value={profile.mother_tongue || ''}
                onChange={handleProfileChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth required>
                <InputLabel>Marital Status</InputLabel>
                <Select
                  name="marital_status"
                  value={profile.marital_status || ''}
                  label="Marital Status"
                  onChange={handleProfileChange}
                >
                  <MenuItem value="never_married">Never Married</MenuItem>
                  <MenuItem value="divorced">Divorced</MenuItem>
                  <MenuItem value="widowed">Widowed</MenuItem>
                  <MenuItem value="separated">Separated</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="About Me"
                name="about_me"
                multiline
                rows={4}
                value={profile.about_me || ''}
                onChange={handleProfileChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Occupation"
                name="occupation"
                value={profile.occupation || ''}
                onChange={handleProfileChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Education"
                name="education"
                value={profile.education || ''}
                onChange={handleProfileChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Income Bracket"
                name="income_bracket"
                value={profile.income_bracket || ''}
                onChange={handleProfileChange}
              />
            </Grid>
            <Grid item xs={12} sm={4}>
              <TextField
                fullWidth
                label="City"
                name="location_city"
                value={profile.location_city || ''}
                onChange={handleProfileChange}
              />
            </Grid>
            <Grid item xs={12} sm={4}>
              <TextField
                fullWidth
                label="State/Province"
                name="location_state"
                value={profile.location_state || ''}
                onChange={handleProfileChange}
              />
            </Grid>
            <Grid item xs={12} sm={4}>
              <TextField
                fullWidth
                label="Country"
                name="location_country"
                value={profile.location_country || ''}
                onChange={handleProfileChange}
              />
            </Grid>
            <Grid item xs={12}>
              <Button
                variant="contained"
                color="primary"
                onClick={saveProfile}
                disabled={saving}
              >
                {saving ? 'Saving...' : 'Save Profile'}
              </Button>
            </Grid>
          </Grid>
        </TabPanel>
        
        {/* Photos Tab */}
        <TabPanel value={tabValue} index={1}>
          <Box sx={{ mb: 3 }}>
            <input
              accept="image/*"
              style={{ display: 'none' }}
              id="photo-upload"
              type="file"
              onChange={handlePhotoUpload}
              disabled={uploadingPhoto}
            />
            <label htmlFor="photo-upload">
              <Button
                variant="contained"
                component="span"
                startIcon={<PhotoCamera />}
                disabled={uploadingPhoto}
              >
                {uploadingPhoto ? 'Uploading...' : 'Upload Photo'}
              </Button>
            </label>
          </Box>
          
          <Grid container spacing={2}>
            {photos.length > 0 ? (
              photos.map((photo) => (
                <Grid item xs={12} sm={6} md={4} key={photo.photo_id}>
                  <Card>
                    <CardMedia
                      component="img"
                      height="200"
                      image={photo.photo_url}
                      alt="Profile photo"
                    />
                    <CardActions>
                      {photo.is_primary && (
                        <Typography variant="caption" color="primary">
                          Primary Photo
                        </Typography>
                      )}
                      <IconButton
                        color="error"
                        onClick={() => handleDeletePhoto(photo.photo_id)}
                      >
                        <Delete />
                      </IconButton>
                    </CardActions>
                  </Card>
                </Grid>
              ))
            ) : (
              <Grid item xs={12}>
                <Typography>No photos uploaded yet. Upload your first photo!</Typography>
              </Grid>
            )}
          </Grid>
        </TabPanel>
        
        {/* Partner Preferences Tab */}
        <TabPanel value={tabValue} index={2}>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Minimum Age"
                name="min_age"
                type="number"
                value={preferences.min_age || ''}
                onChange={handlePreferencesChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Maximum Age"
                name="max_age"
                type="number"
                value={preferences.max_age || ''}
                onChange={handlePreferencesChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Minimum Height (cm)"
                name="height_min"
                type="number"
                value={preferences.height_min || ''}
                onChange={handlePreferencesChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Maximum Height (cm)"
                name="height_max"
                type="number"
                value={preferences.height_max || ''}
                onChange={handlePreferencesChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Religion"
                name="religion"
                value={preferences.religion || ''}
                onChange={handlePreferencesChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Caste Preferences"
                name="caste_preferences"
                value={preferences.caste_preferences || ''}
                onChange={handlePreferencesChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Education Level"
                name="education_level"
                value={preferences.education_level || ''}
                onChange={handlePreferencesChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Minimum Income"
                name="income_min"
                type="number"
                value={preferences.income_min || ''}
                onChange={handlePreferencesChange}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Location Preferences"
                name="location_preferences"
                value={preferences.location_preferences || ''}
                onChange={handlePreferencesChange}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Other Preferences"
                name="other_preferences"
                multiline
                rows={4}
                value={preferences.other_preferences || ''}
                onChange={handlePreferencesChange}
              />
            </Grid>
            <Grid item xs={12}>
              <Button
                variant="contained"
                color="primary"
                onClick={savePreferences}
                disabled={saving}
              >
                {saving ? 'Saving...' : 'Save Preferences'}
              </Button>
            </Grid>
          </Grid>
        </TabPanel>
        
        {/* Family Details Tab */}
        <TabPanel value={tabValue} index={3}>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Father's Occupation"
                name="father_occupation"
                value={familyDetails.father_occupation || ''}
                onChange={handleFamilyChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Mother's Occupation"
                name="mother_occupation"
                value={familyDetails.mother_occupation || ''}
                onChange={handleFamilyChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Number of Siblings"
                name="siblings_count"
                type="number"
                value={familyDetails.siblings_count || ''}
                onChange={handleFamilyChange}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>Family Type</InputLabel>
                <Select
                  name="family_type"
                  value={familyDetails.family_type || ''}
                  label="Family Type"
                  onChange={handleFamilyChange}
                >
                  <MenuItem value="nuclear">Nuclear</MenuItem>
                  <MenuItem value="joint">Joint</MenuItem>
                  <MenuItem value="other">Other</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>Family Values</InputLabel>
                <Select
                  name="family_values"
                  value={familyDetails.family_values || ''}
                  label="Family Values"
                  onChange={handleFamilyChange}
                >
                  <MenuItem value="traditional">Traditional</MenuItem>
                  <MenuItem value="moderate">Moderate</MenuItem>
                  <MenuItem value="liberal">Liberal</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="About Family"
                name="about_family"
                multiline
                rows={4}
                value={familyDetails.about_family || ''}
                onChange={handleFamilyChange}
              />
            </Grid>
            <Grid item xs={12}>
              <Button
                variant="contained"
                color="primary"
                onClick={saveFamilyDetails}
                disabled={saving}
              >
                {saving ? 'Saving...' : 'Save Family Details'}
              </Button>
            </Grid>
          </Grid>
        </TabPanel>
      </Paper>
      
      <Snackbar
        open={notification.open}
        autoHideDuration={6000}
        onClose={handleCloseNotification}
      >
        <Alert onClose={handleCloseNotification} severity={notification.severity}>
          {notification.message}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default ProfilePage;




