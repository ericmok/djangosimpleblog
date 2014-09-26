module.exports = function(grunt) {

    require('time-grunt')(grunt);    
    require('load-grunt-tasks')(grunt);

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        sass: {
            dist: {
                files: {
                    
                }
            }
        }
    });

    grunt.registerTask('default', []); 
};
