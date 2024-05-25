"use client";
import * as React from "react";
import { useState, useRef, useEffect } from 'react';
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
import { blueGrey } from "@mui/material/colors";
import styles from "./page.module.css";
import { theme } from "./components/theme";

  
export default function Home() {
  const isMobile = useMediaQuery("(max-width: 700px)");
  const primary_color = theme.palette.primary;
  // setState for responsive frontend to any backend calls
  const [tempMsg, settempMsg] = useState("");
  const updateTempMsg = (newMsg: React.SetStateAction<string>) => {
    settempMsg(newMsg);
  };

  // State for search query and suggestions
  const [searchQuery, setSearchQuery] = useState("");
  const [suggestions, setSuggestions] = useState([]);

  // Function to handle input changes
  const handleInputChange = async (event) => {
    const query = event.target.value;
    setSearchQuery(query);

    if (query.length > 0) {
      // Fetch suggestions from the backend
      try {
        const response = await fetch(`http://localhost:5000/api/search?query=${query}`);
        const data = await response.json();

        const filteredSuggestions = data.filter(suggestion =>
          suggestion.toLowerCase().startsWith(query.toLowerCase())
        );

        setSuggestions(filteredSuggestions);
      } catch (error) {
        console.error("Error fetching suggestions:", error);
      }
    } else {
      setSuggestions([]);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setSearchQuery(suggestion);
    setSuggestions([]);
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
          <Paper sx={{ backgroundColor: primary_color.light }} elevation={10}>
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
                backgroundColor: primary_color.light,
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
                Predicted Genre:
                </h1>
                <Typography variant="h5" sx={{ margin: "10px" }}>
                  {/* Temporary message for now, reacts to backend responses */}
                  {tempMsg}
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
                      <ListItemButton onClick={() => handleSuggestionClick(suggestion)}>
                        {/* {`${suggestion.track} - ${suggestion.artist}`} */}
                        {suggestion}
                      </ListItemButton>
                    </ListItem>
                  ))}
                </List>
              </div>
            </Paper>
          </Stack>
        </Stack>
      </Box>
    </ThemeProvider>
  );
}