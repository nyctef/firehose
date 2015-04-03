from unittest import TestCase, main

class Tests(TestCase):
    def test_environment_is_sane(self):
        self.assertEqual(1, 1)

if __name__ == '__main__':
    main()
