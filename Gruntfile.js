module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    uglify: {
      options: {
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
      },
      build: {
        src: 'src/<%= pkg.name %>.js',
        dest: 'build/<%= pkg.name %>.min.js'
      }
    },
    bower: {
        dev: {
            base: 'bower_components', /* the path to the bower_components directory */
            dest: 'web/bower_components',
            options: {
                checkExistence: true,
                debugging: true,
                paths: {
                    bowerDirectory: 'bower_components',
                    bowerrc: '.bowerrc',
                    bowerJson: 'bower.json'
                }
            }
        },
        flat: { /* flat folder/file structure */
            dest: 'public/vendor',
            options: {
                debugging: true
            }
        }
    }

  });

  // Load the plugin that provides the "uglify" task.
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('main-bower-files');

  // Default task(s).
  grunt.registerTask('default', ['uglify', 'bower']);

};
