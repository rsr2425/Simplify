import { Typography, Box } from '@mui/material';

function Header() {
  return (
    <Box sx={{ mb: 4 }}>
      <Typography variant="h2" component="h1" align="center">
        Simplifi
      </Typography>
    </Box>
  );
}

export default Header;