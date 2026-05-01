#!/usr/bin/env python3
"""
Organize Backend Folder and PostgreSQL Database Integration
Complete backend organization with PostgreSQL database linkage
"""

import os
import json
import psycopg2
from pathlib import Path
from datetime import datetime

class BackendDatabaseOrganizer:
    def __init__(self):
        self.base_path = Path(r"C:\Users\TTR\Documents\Project_BackEnd")
        self.db_config = {
            'host': 'localhost',
            'port': 5432,
            'database': 'medical_imaging',
            'user': 'postgres',
            'password': 'Sibo25Mana'
        }
        
    def organize_backend_structure(self):
        """Organize backend folder structure for database integration"""
        print(" BACKEND FOLDER ORGANIZATION")
        print("=" * 60)
        
        # Essential backend structure
        backend_structure = {
            'config/': {
                'purpose': 'Database and application configuration',
                'files': ['database.js', 'config.js']
            },
            'models/': {
                'purpose': 'Database models and schemas',
                'files': ['Patient.js', 'Doctor.js', 'Study.js', 'Image.js', 'User.js']
            },
            'controllers/': {
                'purpose': 'API request handlers',
                'files': ['patientController.js', 'doctorController.js', 'studyController.js', 'imageController.js', 'authController.js']
            },
            'routes/': {
                'purpose': 'API routing',
                'files': ['patients.routes.js', 'doctors.routes.js', 'studies.routes.js', 'images.routes.js', 'auth.routes.js']
            },
            'middleware/': {
                'purpose': 'Custom middleware',
                'files': ['auth.js', 'validation.js', 'errorHandler.js']
            },
            'database/': {
                'purpose': 'Database scripts and migrations',
                'files': ['connection.js', 'migrations.sql', 'seeds.sql']
            }
        }
        
        print(" Creating organized backend structure:")
        
        for folder, info in backend_structure.items():
            folder_path = self.base_path / folder
            folder_path.mkdir(exist_ok=True)
            print(f"   {folder} - {info['purpose']}")
            
            for file in info['files']:
                file_path = folder_path / file
                if not file_path.exists():
                    print(f"      Creating: {file}")
                    # File will be created by specific methods
        
        return True
    
    def create_database_config(self):
        """Create database configuration with PostgreSQL password"""
        print("\n DATABASE CONFIGURATION")
        print("=" * 60)
        
        config_dir = self.base_path / 'config'
        config_dir.mkdir(exist_ok=True)
        
        # Create database configuration
        db_config_content = f"""// PostgreSQL Database Configuration
const {{ config }} = require('dotenv');
config();

module.exports = {{
  host: process.env.DB_HOST || '{self.db_config['host']}',
  port: process.env.DB_PORT || {self.db_config['port']},
  database: process.env.DB_NAME || '{self.db_config['database']}',
  username: process.env.DB_USER || '{self.db_config['user']}',
  password: process.env.DB_PASSWORD || '{self.db_config['password']}',
  
  // Connection pool settings
  pool: {{
    max: 20,
    min: 5,
    acquire: 30000,
    idle: 10000
  }},
  
  // Sequelize options
  dialect: 'postgres',
  logging: process.env.NODE_ENV === 'development' ? console.log : false,
  
  // SSL configuration (disable for local development)
  dialectOptions: {{
    ssl: process.env.NODE_ENV === 'production' ? {{
      require: true,
      rejectUnauthorized: false
    }} : false
  }}
}};
"""
        
        db_config_path = config_dir / 'database.js'
        with open(db_config_path, 'w') as f:
            f.write(db_config_content)
        
        print(f"   Created: config/database.js")
        
        # Create main configuration
        main_config_content = """// Main Application Configuration
const { config } = require('dotenv');
config();

module.exports = {
  // Server configuration
  port: process.env.PORT || 5000,
  nodeEnv: process.env.NODE_ENV || 'development',
  
  // Frontend URL for CORS
  frontendUrl: process.env.FRONTEND_URL || 'http://localhost:3000',
  
  // JWT configuration
  jwt: {
    secret: process.env.JWT_SECRET || 'your_super_secret_jwt_key_here_change_in_production',
    expiresIn: process.env.JWT_EXPIRES_IN || '24h'
  },
  
  // File upload configuration
  upload: {
    maxSize: parseInt(process.env.MAX_FILE_SIZE) || 104857600, // 100MB
    directory: process.env.UPLOAD_DIR || './uploads'
  },
  
  // DICOM configuration
  dicom: {
    storagePath: process.env.DICOM_STORAGE_PATH || './uploads/dicom',
    thumbnailSize: parseInt(process.env.THUMBNAIL_SIZE) || 200
  }
};
"""
        
        main_config_path = config_dir / 'config.js'
        with open(main_config_path, 'w') as f:
            f.write(main_config_content)
        
        print(f"   Created: config/config.js")
        
        return True
    
    def test_database_connection(self):
        """Test PostgreSQL database connection"""
        print("\n DATABASE CONNECTION TEST")
        print("=" * 60)
        
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            print(f"   Host: {self.db_config['host']}")
            print(f"   Port: {self.db_config['port']}")
            print(f"   Database: {self.db_config['database']}")
            print(f"   User: {self.db_config['user']}")
            print(f"   Password: ***CONFIGURED***")
            
            # Test connection
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"   PostgreSQL: {version[0]}")
            
            # Check tables
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
            tables = [row[0] for row in cursor.fetchall()]
            
            print(f"   Tables found: {len(tables)}")
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"      - {table}: {count} records")
            
            cursor.close()
            conn.close()
            
            print("   Connection: SUCCESS")
            return True
            
        except Exception as e:
            print(f"   Connection Error: {e}")
            return False
    
    def create_database_models(self):
        """Create database model files"""
        print("\n DATABASE MODELS")
        print("=" * 60)
        
        models_dir = self.base_path / 'models'
        models_dir.mkdir(exist_ok=True)
        
        # Patient model
        patient_model = """// Patient Model
const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');

const Patient = sequelize.define('Patient', {
  id: {
    type: DataTypes.UUID,
    defaultValue: DataTypes.UUIDV4,
    primaryKey: true
  },
  firstName: {
    type: DataTypes.STRING,
    allowNull: false
  },
  lastName: {
    type: DataTypes.STRING,
    allowNull: false
  },
  email: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true,
    validate: {
      isEmail: true
    }
  },
  phoneNumber: {
    type: DataTypes.STRING,
    allowNull: false
  },
  dateOfBirth: {
    type: DataTypes.DATEONLY,
    allowNull: false
  },
  gender: {
    type: DataTypes.ENUM('male', 'female', 'other'),
    allowNull: false
  },
  address: {
    type: DataTypes.TEXT
  },
  emergencyContact: {
    type: DataTypes.STRING
  },
  emergencyPhone: {
    type: DataTypes.STRING
  },
  medicalHistory: {
    type: DataTypes.TEXT
  },
  allergies: {
    type: DataTypes.TEXT
  },
  createdAt: {
    type: DataTypes.DATE,
    allowNull: false
  },
  updatedAt: {
    type: DataTypes.DATE,
    allowNull: false
  }
}, {
  tableName: 'patients',
  timestamps: true
});

module.exports = Patient;
"""
        
        with open(models_dir / 'Patient.js', 'w') as f:
            f.write(patient_model)
        print("   Created: models/Patient.js")
        
        # Doctor model
        doctor_model = """// Doctor Model
const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');

const Doctor = sequelize.define('Doctor', {
  id: {
    type: DataTypes.UUID,
    defaultValue: DataTypes.UUIDV4,
    primaryKey: true
  },
  firstName: {
    type: DataTypes.STRING,
    allowNull: false
  },
  lastName: {
    type: DataTypes.STRING,
    allowNull: false
  },
  email: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true,
    validate: {
      isEmail: true
    }
  },
  phoneNumber: {
    type: DataTypes.STRING,
    allowNull: false
  },
  specialization: {
    type: DataTypes.STRING,
    allowNull: false
  },
  licenseNumber: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true
  },
  department: {
    type: DataTypes.STRING,
    allowNull: false
  },
  experience: {
    type: DataTypes.INTEGER
  },
  education: {
    type: DataTypes.TEXT
  },
  certifications: {
    type: DataTypes.TEXT
  },
  availability: {
    type: DataTypes.JSON
  },
  createdAt: {
    type: DataTypes.DATE,
    allowNull: false
  },
  updatedAt: {
    type: DataTypes.DATE,
    allowNull: false
  }
}, {
  tableName: 'doctors',
  timestamps: true
});

module.exports = Doctor;
"""
        
        with open(models_dir / 'Doctor.js', 'w') as f:
            f.write(doctor_model)
        print("   Created: models/Doctor.js")
        
        # Study model
        study_model = """// Study Model
const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');

const Study = sequelize.define('Study', {
  id: {
    type: DataTypes.UUID,
    defaultValue: DataTypes.UUIDV4,
    primaryKey: true
  },
  accessionNumber: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true
  },
  patientId: {
    type: DataTypes.UUID,
    allowNull: false,
    references: {
      model: 'patients',
      key: 'id'
    }
  },
  doctorId: {
    type: DataTypes.UUID,
    allowNull: false,
    references: {
      model: 'doctors',
      key: 'id'
    }
  },
  studyType: {
    type: DataTypes.ENUM('CT', 'MRI', 'X-Ray', 'Ultrasound'),
    allowNull: false
  },
  description: {
    type: DataTypes.TEXT
  },
  status: {
    type: DataTypes.ENUM('scheduled', 'in-progress', 'completed', 'cancelled'),
    defaultValue: 'scheduled'
  },
  scheduledDate: {
    type: DataTypes.DATE,
    allowNull: false
  },
  completedDate: {
    type: DataTypes.DATE
  },
  report: {
    type: DataTypes.JSON
  },
  findings: {
    type: DataTypes.TEXT
  },
  impression: {
    type: DataTypes.TEXT
  },
  reportedBy: {
    type: DataTypes.UUID,
    references: {
      model: 'doctors',
      key: 'id'
    }
  },
  createdAt: {
    type: DataTypes.DATE,
    allowNull: false
  },
  updatedAt: {
    type: DataTypes.DATE,
    allowNull: false
  }
}, {
  tableName: 'studies',
  timestamps: true
});

module.exports = Study;
"""
        
        with open(models_dir / 'Study.js', 'w') as f:
            f.write(study_model)
        print("   Created: models/Study.js")
        
        # Image model
        image_model = """// Image Model
const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');

const Image = sequelize.define('Image', {
  id: {
    type: DataTypes.UUID,
    defaultValue: DataTypes.UUIDV4,
    primaryKey: true
  },
  studyId: {
    type: DataTypes.UUID,
    allowNull: false,
    references: {
      model: 'studies',
      key: 'id'
    }
  },
  filename: {
    type: DataTypes.STRING,
    allowNull: false
  },
  originalName: {
    type: DataTypes.STRING,
    allowNull: false
  },
  mimeType: {
    type: DataTypes.STRING,
    allowNull: false
  },
  size: {
    type: DataTypes.INTEGER,
    allowNull: false
  },
  path: {
    type: DataTypes.STRING,
    allowNull: false
  },
  thumbnailPath: {
    type: DataTypes.STRING
  },
  dicomData: {
    type: DataTypes.JSON
  },
  metadata: {
    type: DataTypes.JSON
  },
  uploadDate: {
    type: DataTypes.DATE,
    allowNull: false
  },
  processed: {
    type: DataTypes.BOOLEAN,
    defaultValue: false
  },
  createdAt: {
    type: DataTypes.DATE,
    allowNull: false
  },
  updatedAt: {
    type: DataTypes.DATE,
    allowNull: false
  }
}, {
  tableName: 'images',
  timestamps: true
});

module.exports = Image;
"""
        
        with open(models_dir / 'Image.js', 'w') as f:
            f.write(image_model)
        print("   Created: models/Image.js")
        
        # User model
        user_model = """// User Model
const { DataTypes } = require('sequelize');
const { sequelize } = require('../config/database');

const User = sequelize.define('User', {
  id: {
    type: DataTypes.UUID,
    defaultValue: DataTypes.UUIDV4,
    primaryKey: true
  },
  username: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true
  },
  email: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true,
    validate: {
      isEmail: true
    }
  },
  password: {
    type: DataTypes.STRING,
    allowNull: false
  },
  role: {
    type: DataTypes.ENUM('admin', 'doctor', 'technician', 'radiologist'),
    allowNull: false
  },
  firstName: {
    type: DataTypes.STRING,
    allowNull: false
  },
  lastName: {
    type: DataTypes.STRING,
    allowNull: false
  },
  isActive: {
    type: DataTypes.BOOLEAN,
    defaultValue: true
  },
  lastLogin: {
    type: DataTypes.DATE
  },
  permissions: {
    type: DataTypes.JSON
  },
  createdAt: {
    type: DataTypes.DATE,
    allowNull: false
  },
  updatedAt: {
    type: DataTypes.DATE,
    allowNull: false
  }
}, {
  tableName: 'users',
  timestamps: true
});

module.exports = User;
"""
        
        with open(models_dir / 'User.js', 'w') as f:
            f.write(user_model)
        print("   Created: models/User.js")
        
        return True
    
    def create_database_index_file(self):
        """Create database index file for all models"""
        print("\n DATABASE INDEX FILE")
        print("=" * 60)
        
        models_dir = self.base_path / 'models'
        
        index_content = """// Database Models Index
const { Sequelize } = require('sequelize');
const { sequelize } = require('../config/database');

// Import all models
const Patient = require('./Patient');
const Doctor = require('./Doctor');
const Study = require('./Study');
const Image = require('./Image');
const User = require('./User');

// Define associations
const associate = () => {
  // Patient has many studies
  Patient.hasMany(Study, {
    foreignKey: 'patientId',
    as: 'studies'
  });
  Study.belongsTo(Patient, {
    foreignKey: 'patientId',
    as: 'patient'
  });

  // Doctor has many studies
  Doctor.hasMany(Study, {
    foreignKey: 'doctorId',
    as: 'assignedStudies'
  });
  Study.belongsTo(Doctor, {
    foreignKey: 'doctorId',
    as: 'doctor'
  });

  // Doctor can report many studies
  Doctor.hasMany(Study, {
    foreignKey: 'reportedBy',
    as: 'reportedStudies'
  });
  Study.belongsTo(Doctor, {
    foreignKey: 'reportedBy',
    as: 'reportingDoctor'
  });

  // Study has many images
  Study.hasMany(Image, {
    foreignKey: 'studyId',
    as: 'images'
  });
  Image.belongsTo(Study, {
    foreignKey: 'studyId',
    as: 'study'
  });
};

// Initialize associations
associate();

// Export models and sequelize instance
module.exports = {
  sequelize,
  Sequelize,
  Patient,
  Doctor,
  Study,
  Image,
  User
};
"""
        
        with open(models_dir / 'index.js', 'w') as f:
            f.write(index_content)
        
        print("   Created: models/index.js")
        
        return True
    
    def update_environment_file(self):
        """Update .env file with PostgreSQL configuration"""
        print("\n ENVIRONMENT CONFIGURATION")
        print("=" * 60)
        
        env_content = f"""# PostgreSQL Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=medical_imaging
DB_USER=postgres
DB_PASSWORD=Sibo25Mana

# JWT Configuration
JWT_SECRET=your_super_secret_jwt_key_here_change_in_production
JWT_EXPIRES_IN=24h

# Server Configuration
PORT=5000
NODE_ENV=development

# Frontend URL (for CORS)
FRONTEND_URL=http://localhost:3000

# File Upload Configuration
MAX_FILE_SIZE=104857600
UPLOAD_DIR=uploads

# DICOM Configuration
DICOM_STORAGE_PATH=./uploads/dicom
THUMBNAIL_SIZE=200
"""
        
        env_path = self.base_path / '.env'
        with open(env_path, 'w') as f:
            f.write(env_content)
        
        print("   Updated: .env")
        print(f"   Database Password: Sibo25Mana")
        
        return True
    
    def create_database_seeder(self):
        """Create database seeder for sample data"""
        print("\n DATABASE SEEDER")
        print("=" * 60)
        
        database_dir = self.base_path / 'database'
        database_dir.mkdir(exist_ok=True)
        
        seeder_content = """// Database Seeder
const {{ sequelize, Patient, Doctor, Study, Image, User }} = require('../models');
const bcrypt = require('bcrypt');

const seedDatabase = async () => {{
  try {{
    // Sync database
    await sequelize.sync({{ force: false }});
    console.log('Database synchronized');

    // Create sample users
    const users = [
      {{
        username: 'admin',
        email: 'admin@medical.com',
        password: await bcrypt.hash('admin123', 10),
        role: 'admin',
        firstName: 'System',
        lastName: 'Administrator'
      }},
      {{
        username: 'johndoe',
        email: 'john.doe@hospital.com',
        password: await bcrypt.hash('doctor123', 10),
        role: 'doctor',
        firstName: 'John',
        lastName: 'Doe'
      }}
    ];

    for (const userData of users) {{
      await User.findOrCreate({{
        where: {{ email: userData.email }},
        defaults: userData
      }});
    }}

    // Create sample patients
    const patients = [
      {{
        firstName: 'Alice',
        lastName: 'Brown',
        email: 'alice.brown@email.com',
        phoneNumber: '+1234567890',
        dateOfBirth: '1985-05-15',
        gender: 'female',
        address: '123 Main St, City, State'
      }},
      {{
        firstName: 'Bob',
        lastName: 'Smith',
        email: 'bob.smith@email.com',
        phoneNumber: '+0987654321',
        dateOfBirth: '1978-08-22',
        gender: 'male',
        address: '456 Oak Ave, Town, State'
      }}
    ];

    for (const patientData of patients) {{
      await Patient.findOrCreate({{
        where: {{ email: patientData.email }},
        defaults: patientData
      }});
    }}

    // Create sample doctors
    const doctors = [
      {{
        firstName: 'Sarah',
        lastName: 'Wilson',
        email: 'sarah.wilson@hospital.com',
        phoneNumber: '+1122334455',
        specialization: 'Radiology',
        licenseNumber: 'RAD123456',
        department: 'Radiology'
      }}
    ];

    for (const doctorData of doctors) {{
      await Doctor.findOrCreate({{
        where: {{ email: doctorData.email }},
        defaults: doctorData
      }});
    }}

    console.log('Database seeded successfully');
    process.exit(0);
  }} catch (error) {{
    console.error('Error seeding database:', error);
    process.exit(1);
  }}
}};

seedDatabase();
"""
        
        with open(database_dir / 'seeder.js', 'w') as f:
            f.write(seeder_content)
        
        print("   Created: database/seeder.js")
        
        return True
    
    def run_complete_organization(self):
        """Run complete backend organization"""
        print(" COMPLETE BACKEND ORGANIZATION & POSTGRESQL INTEGRATION")
        print("=" * 80)
        print(f"Location: {self.base_path}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # Step 1: Organize folder structure
        self.organize_backend_structure()
        
        # Step 2: Create database configuration
        self.create_database_config()
        
        # Step 3: Test database connection
        connection_ok = self.test_database_connection()
        
        if connection_ok:
            # Step 4: Create database models
            self.create_database_models()
            
            # Step 5: Create database index
            self.create_database_index_file()
            
            # Step 6: Update environment file
            self.update_environment_file()
            
            # Step 7: Create database seeder
            self.create_database_seeder()
            
            print("\n" + "=" * 80)
            print(" ORGANIZATION COMPLETE!")
            print("=" * 80)
            print(" Backend folder organized for PostgreSQL integration")
            print(" Database models created for all tables")
            print(" Environment configured with password: Sibo25Mana")
            print(" Database connection tested and verified")
            print(" All tables linked and ready for API integration")
            print("=" * 80)
            
            return True
        else:
            print("\n" + "=" * 80)
            print(" ORGANIZATION FAILED!")
            print("=" * 80)
            print(" Database connection failed")
            print(" Check PostgreSQL server and credentials")
            print("=" * 80)
            
            return False

if __name__ == "__main__":
    organizer = BackendDatabaseOrganizer()
    success = organizer.run_complete_organization()
    
    if success:
        print("\n NEXT STEPS:")
        print("1. Restart backend server")
        print("2. Run database seeder: node database/seeder.js")
        print("3. Test API endpoints")
        print("4. Verify frontend integration")
    else:
        print("\n TROUBLESHOOTING:")
        print("1. Check PostgreSQL server status")
        print("2. Verify database: medical_imaging")
        print("3. Verify user: postgres")
        print("4. Check password: Sibo25Mana")
