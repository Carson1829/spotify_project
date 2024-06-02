"use client";
import * as React from "react";
import { useState } from 'react';
//import Canvas from "./components/canvas";
import {
  Box,
  Paper,
  Typography,
  Stack,
  useMediaQuery,
  ThemeProvider,
  TextField,
  List,
  ListItem,
  ListItemButton
} from "@mui/material/";
import styles from "./page.module.css";
import { theme } from "./components/theme";

  
export default function Home() {
  const isMobile = useMediaQuery("(max-width: 700px)");
  const primary_color = theme.palette.primary;
  // setState for responsive frontend to any backend calls

  const [searchQuery, setSearchQuery] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [selectedSong, setSelectedSong] = useState("");
  const [predictedGenres, setPredictedGenres] = useState("");

  // function to handle input changes in search bar
  const handleInputChange = async (event) => {
    const query = event.target.value;
    setSearchQuery(query);
  
    if (query.length > 0) {
      try {
        const response = await fetch(`http://localhost:5000/api/search?query=${query}`);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
  
        const filteredSuggestions = data.filter(suggestion =>
          suggestion.track.toLowerCase().startsWith(query.toLowerCase())
        );
  
        setSuggestions(filteredSuggestions);
      } catch (error) {
        console.error("Error fetching suggestions:", error);
      }
    } else {
      setSuggestions([]);
    }
  };

  // function to handle clicks on suggestion list
  const handleSuggestionClick = async (suggestion) => {
    console.log('Suggestion clicked:', suggestion);
    const track = suggestion.suggestion.track;
    const artist = suggestion.suggestion.artist;

    setSearchQuery('');
    setSuggestions([]);
    setSelectedSong(`${track} - ${artist}`);
    
    try {
      const response = await fetch('http://localhost:5000/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ track: track, artist: artist }),
      });
      
      console.log('Response status:', response.status);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      
      const data = await response.json();
      console.log('Received data:', data);
      setPredictedGenres(data.genres);
    } catch (error) {
      console.error("Error fetching prediction:", error);
    }
  };
  

  return (
    <ThemeProvider theme={theme}>
      <Box
        sx={{ width: "98%", height: "100%" }}
        margin={"1%"}
        justifyContent="center"
      >
        <Stack
          spacing={3}
          sx={{ height: "95%" }}
          padding={1}
          justifyContent="center"
        >
          <Paper sx={{ backgroundColor: primary_color.main }} elevation={10}>
            <Typography variant="h2" margin={2} className={styles.heading}>
              ECS 171 song genre prediction
            </Typography>
          </Paper>
          <Stack
            direction={{ xs: "column", sm: "row" }}
            spacing={2}
            sx={{ height: "100%" }}
            justifyContent="center"
          >
            <Paper
              sx={{
                backgroundColor: primary_color.main,
                height: "100%",
                padding: { xs: 0, sm: 2 },
                width: { xs: "100%", sm: "20%" }
              }}
              elevation={5}
            >
              <div
                style={
                  isMobile
                    ? {
                        display: "flex",
                        flexDirection: "column",
                        justifyContent: "center",
                        alignItems: "center"
                      }
                    : {}
                }
              >
                <h1>
                Song chosen:
                </h1>
                <Typography variant="body1" sx={{ margin: "10px" }}>
                  {selectedSong}
                </Typography>

                {/* Search Bar */}
                <TextField
                  label="Search Songs"
                  variant="outlined"
                  value={searchQuery}
                  onChange={handleInputChange}
                  sx={{ width: '100%', marginTop: 2 }}
                />

                {/* Suggestions List */}
                <List>
                  {suggestions.map((suggestion, index) => (
                    <ListItem key={index} disablePadding>
                      <ListItemButton onClick={() => handleSuggestionClick({suggestion})}>
                        {`${suggestion.track} - ${suggestion.artist}`}
                      </ListItemButton>
                    </ListItem>
                  ))}
                </List>
              </div>
            </Paper>

            {/* section displaying predicted genre*/}
            <Paper sx={{ backgroundColor: primary_color.main, height: "100%", padding: { xs: 0, sm: 2 }, width: { xs: "100%", sm: "20%" } }} elevation={5}>
              <Typography variant="h6" sx={{ margin: "10px" }}>
                Predicted genres:
              </Typography>
              <Typography variant="h5" sx={{ margin: "10px" }}>
                {/* reacts to backend responses */}
                {predictedGenres}
              </Typography>
            </Paper>
          </Stack>
        </Stack>
      </Box>
    </ThemeProvider>
  );
}