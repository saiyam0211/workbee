// Utility functions for localStorage operations with better error handling and persistence

const STORAGE_KEY = 'wb_saved_jobs';

export const storageUtils = {
  // Get saved jobs with error handling
  getSavedJobs: () => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return {};
      
      const parsed = JSON.parse(raw);
      console.log('Retrieved saved jobs:', parsed); // Debug log
      return parsed;
    } catch (error) {
      console.error('Error retrieving saved jobs:', error);
      return {};
    }
  },

  // Save jobs with error handling
  saveJobs: (jobs) => {
    try {
      const jsonString = JSON.stringify(jobs);
      localStorage.setItem(STORAGE_KEY, jsonString);
      console.log('Saved jobs to localStorage:', jobs); // Debug log
      
      // Verify the save was successful
      const retrieved = localStorage.getItem(STORAGE_KEY);
      if (retrieved === jsonString) {
        console.log('Save verification successful');
        return true;
      } else {
        console.error('Save verification failed');
        return false;
      }
    } catch (error) {
      console.error('Error saving jobs:', error);
      return false;
    }
  },

  // Add a job to saved jobs
  addJob: (job) => {
    try {
      const saved = storageUtils.getSavedJobs();
      const company = job.company || 'Unknown';
      const jobKey = `${company}__${job.title}`;
      
      if (!saved[company]) {
        saved[company] = {};
      }
      
      saved[company][jobKey] = {
        ...job,
        savedAt: new Date().toISOString(),
        id: jobKey
      };
      
      const success = storageUtils.saveJobs(saved);
      if (success) {
        // Dispatch event to notify other components
        window.dispatchEvent(new CustomEvent('wb:saved-jobs-updated'));
      }
      return success;
    } catch (error) {
      console.error('Error adding job:', error);
      return false;
    }
  },

  // Remove a job from saved jobs
  removeJob: (job, companyName) => {
    try {
      const saved = storageUtils.getSavedJobs();
      const jobKey = `${companyName}__${job.title}`;
      
      if (saved[companyName] && saved[companyName][jobKey]) {
        delete saved[companyName][jobKey];
        
        // Clean up empty company entries
        if (Object.keys(saved[companyName]).length === 0) {
          delete saved[companyName];
        }
        
        const success = storageUtils.saveJobs(saved);
        if (success) {
          // Dispatch event to notify other components
          window.dispatchEvent(new CustomEvent('wb:saved-jobs-updated'));
        }
        return success;
      }
      return false;
    } catch (error) {
      console.error('Error removing job:', error);
      return false;
    }
  },

  // Check if a job is saved
  isJobSaved: (job) => {
    try {
      const saved = storageUtils.getSavedJobs();
      const company = job.company || 'Unknown';
      const jobKey = `${company}__${job.title}`;
      
      return !!(saved[company] && saved[company][jobKey]);
    } catch (error) {
      console.error('Error checking if job is saved:', error);
      return false;
    }
  },

  // Get saved jobs count for a company
  getCompanyJobCount: (companyName) => {
    try {
      const saved = storageUtils.getSavedJobs();
      return Object.keys(saved[companyName] || {}).length;
    } catch (error) {
      console.error('Error getting company job count:', error);
      return 0;
    }
  },

  // Get all saved jobs for a company
  getCompanyJobs: (companyName) => {
    try {
      const saved = storageUtils.getSavedJobs();
      const companyMap = saved[companyName] || {};
      return Object.values(companyMap);
    } catch (error) {
      console.error('Error getting company jobs:', error);
      return [];
    }
  },

  // Get all saved job counts
  getAllJobCounts: () => {
    try {
      const saved = storageUtils.getSavedJobs();
      const counts = {};
      Object.keys(saved).forEach((company) => {
        counts[company] = Object.keys(saved[company] || {}).length;
      });
      return counts;
    } catch (error) {
      console.error('Error getting all job counts:', error);
      return {};
    }
  },

  // Clear all saved jobs (for testing)
  clearAllJobs: () => {
    try {
      localStorage.removeItem(STORAGE_KEY);
      window.dispatchEvent(new CustomEvent('wb:saved-jobs-updated'));
      console.log('Cleared all saved jobs');
      return true;
    } catch (error) {
      console.error('Error clearing all jobs:', error);
      return false;
    }
  },

  // Get storage info for debugging
  getStorageInfo: () => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      const size = raw ? new Blob([raw]).size : 0;
      return {
        hasData: !!raw,
        size: size,
        sizeKB: (size / 1024).toFixed(2),
        companies: Object.keys(storageUtils.getSavedJobs()).length
      };
    } catch (error) {
      console.error('Error getting storage info:', error);
      return { hasData: false, size: 0, sizeKB: '0', companies: 0 };
    }
  },

  // Tour utilities
  tourUtils: {
    // Check if user has completed the tour
    hasCompletedTour: () => {
      try {
        return localStorage.getItem('workbee-tour-completed') === 'true';
      } catch (error) {
        console.error('Error checking tour completion:', error);
        return false;
      }
    },

    // Mark tour as completed
    markTourCompleted: () => {
      try {
        localStorage.setItem('workbee-tour-completed', 'true');
        return true;
      } catch (error) {
        console.error('Error marking tour as completed:', error);
        return false;
      }
    },

    // Reset tour (for testing purposes)
    resetTour: () => {
      try {
        localStorage.removeItem('workbee-tour-completed');
        return true;
      } catch (error) {
        console.error('Error resetting tour:', error);
        return false;
      }
    }
  }
};

// Make it available globally for debugging
if (typeof window !== 'undefined') {
  window.storageUtils = storageUtils;
}
