


import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Typography, 
  Box, 
  Grid, 
  Card, 
  CardContent, 
  CardMedia, 
  Button, 
  Container,
  Paper
} from '@mui/material';
import { useAuth } from '../context/AuthContext';
import { successStoryService } from '../services/api';

const HomePage = () => {
  const { currentUser } = useAuth();
  const [featuredStories, setFeaturedStories] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchFeaturedStories = async () => {
      try {
        const response = await successStoryService.getSuccessStories(true, true, 0, 3);
        setFeaturedStories(response.data);
      } catch (error) {
        console.error('Error fetching featured stories:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchFeaturedStories();
  }, []);

  return (
    <Box>
      {/* Hero Section */}
      <Paper
        sx={{
          position: 'relative',
          backgroundColor: 'grey.800',
          color: '#fff',
          mb: 4,
          backgroundSize: 'cover',
          backgroundRepeat: 'no-repeat',
          backgroundPosition: 'center',
          backgroundImage: `url('https://source.unsplash.com/random?wedding')`,
          height: '400px',
          display: 'flex',
          alignItems: 'center',
        }}
      >
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            bottom: 0,
            right: 0,
            left: 0,
            backgroundColor: 'rgba(0,0,0,.3)',
          }}
        />
        <Container maxWidth="md">
          <Box sx={{ position: 'relative', p: { xs: 3, md: 6 } }}>
            <Typography component="h1" variant="h2" color="inherit" gutterBottom>
              Find Your Perfect Match
            </Typography>
            <Typography variant="h5" color="inherit" paragraph>
              Join thousands of happy couples who found their soulmate on Milan
            </Typography>
            {!currentUser && (
              <Button variant="contained" color="primary" component={Link} to="/register" size="large">
                Get Started
              </Button>
            )}
          </Box>
        </Container>
      </Paper>

      {/* Features Section */}
      <Container maxWidth="lg">
        <Typography variant="h4" gutterBottom align="center" sx={{ mb: 4 }}>
          Why Choose Milan?
        </Typography>
        <Grid container spacing={4}>
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Typography variant="h5" component="div" gutterBottom>
                  Verified Profiles
                </Typography>
                <Typography variant="body1" color="text.secondary">
                  All profiles are manually verified to ensure authenticity and build trust.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Typography variant="h5" component="div" gutterBottom>
                  Advanced Matching
                </Typography>
                <Typography variant="body1" color="text.secondary">
                  Our intelligent algorithm suggests matches based on your preferences and compatibility.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Typography variant="h5" component="div" gutterBottom>
                  Privacy Control
                </Typography>
                <Typography variant="body1" color="text.secondary">
                  You control who sees your information and when to share contact details.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>

      {/* Success Stories Section */}
      <Box sx={{ bgcolor: 'background.paper', py: 6, mt: 6 }}>
        <Container maxWidth="lg">
          <Typography variant="h4" gutterBottom align="center" sx={{ mb: 4 }}>
            Success Stories
          </Typography>
          <Grid container spacing={4}>
            {featuredStories.length > 0 ? (
              featuredStories.map((story) => (
                <Grid item key={story.story_id} xs={12} md={4}>
                  <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                    <CardMedia
                      component="img"
                      height="200"
                      image="https://source.unsplash.com/random?wedding"
                      alt={story.story_title}
                    />
                    <CardContent sx={{ flexGrow: 1 }}>
                      <Typography gutterBottom variant="h5" component="h2">
                        {story.story_title}
                      </Typography>
                      <Typography>
                        {story.story_content.substring(0, 100)}...
                      </Typography>
                    </CardContent>
                    <Box sx={{ p: 2 }}>
                      <Button component={Link} to={`/success-stories/${story.story_id}`}>
                        Read More
                      </Button>
                    </Box>
                  </Card>
                </Grid>
              ))
            ) : (
              <Box sx={{ textAlign: 'center', width: '100%', py: 4 }}>
                <Typography variant="body1">
                  {loading ? 'Loading success stories...' : 'No success stories yet. Be the first to share your story!'}
                </Typography>
              </Box>
            )}
          </Grid>
          <Box sx={{ textAlign: 'center', mt: 4 }}>
            <Button variant="outlined" component={Link} to="/success-stories">
              View All Success Stories
            </Button>
          </Box>
        </Container>
      </Box>

      {/* Call to Action */}
      <Container maxWidth="md" sx={{ my: 6, textAlign: 'center' }}>
        <Typography variant="h4" gutterBottom>
          Ready to find your perfect match?
        </Typography>
        <Typography variant="body1" paragraph>
          Join thousands of happy couples who found their soulmate on Milan.
        </Typography>
        {!currentUser ? (
          <Button variant="contained" color="primary" component={Link} to="/register" size="large">
            Register Now
          </Button>
        ) : (
          <Button variant="contained" color="primary" component={Link} to="/matches" size="large">
            Find Matches
          </Button>
        )}
      </Container>
    </Box>
  );
};

export default HomePage;


