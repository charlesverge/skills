if [ ! -d beanie ] ; then
  git clone git@github.com:BeanieODM/beanie.git
else
  cd beanie && git pull origin main
  cd ..
fi
rsync -av beanie/docs/ resources/docs/
