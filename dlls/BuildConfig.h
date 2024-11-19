//======================================================================================================
// Copyright 2013, NaturalPoint Inc.
//======================================================================================================
#pragma once

//== Static & Dynamic Linking Preprocessor Defines

#ifdef CORE_EXPORTS
    #define CORE_API __declspec(dllexport)
#elif defined CORE_IMPORTS
    #define CORE_API __declspec(dllimport)
#else
    #define CORE_API
#endif

//== Global System Selection

#ifdef _DEBUG           //=== DEBUG BUILD SETTINGS =====================================================

#define ENABLE_CORE_DEBUGSYSTEM   1 //=== Enable/Disable Debug System for debug builds
#define ENABLE_CORE_DEBUGLOGGING  0 //=== Enable/Disable Debug System output C:\\Users\\Public\\Documents\\DebugLog.txt

#else                   //=== RELEASE BUILD SETTINGS ===================================================

#define ENABLE_CORE_DEBUGSYSTEM   0 //=== Enable/Disable Debug System for debug builds
#define ENABLE_CORE_DEBUGLOGGING  0 //=== Enable/Disable Debug System output C:\\Users\\Public\\Documents\\DebugLog.txt

#endif

//== Enable Systems based on selection above

#if ENABLE_CORE_DEBUGSYSTEM==1
#define CORE_DEBUGSYSTEM
#else
#undef  CORE_DEBUGSYSTEM
#endif

#if ENABLE_CORE_DEBUGLOGGING==1
#define CORE_DEBUGLOGGING
#else
#undef  CORE_DEBUGLOGGING
#endif
